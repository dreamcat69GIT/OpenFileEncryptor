import io
import warnings
from os import path, remove, urandom

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

version = "1.0.0"

bufferSizeDef = 64 * 1024

maxPassLen = 1024

AESBlockSize = 16


def stretch(passw, iv1):

    digest = iv1 + (16 * b"\x00")

    for i in range(8192):
        passHash = hashes.Hash(hashes.SHA256(), backend=default_backend())
        passHash.update(digest)
        passHash.update(bytes(passw, "utf_16_le"))
        digest = passHash.finalize()

    return digest

def encryptFile(infile, outfile, passw, bufferSize=bufferSizeDef):
    try:
        with open(infile, "rb") as fIn:
            if path.isfile(outfile):
                if path.samefile(infile, outfile):
                    raise ValueError("Input and output files are the same.")
            try:
                with open(outfile, "wb") as fOut:
                    # encrypt file stream
                    encryptStream(fIn, fOut, passw, bufferSize)

            except IOError:
                raise ValueError("Unable to write output file.")

    except IOError:
        raise ValueError("Unable to read input file.")

def encryptStream(fIn, fOut, passw, bufferSize=bufferSizeDef):
    if bufferSize % AESBlockSize != 0:
        raise ValueError("Buffer size must be a multiple of AES block size.")

    if len(passw) > maxPassLen:
        raise ValueError("Password is too long.")

    iv1 = urandom(AESBlockSize)

    key = stretch(passw, iv1)

    iv0 = urandom(AESBlockSize)

    intKey = urandom(32)

    cipher0 = Cipher(algorithms.AES(intKey), modes.CBC(iv0), backend=default_backend())
    encryptor0 = cipher0.encryptor()

    hmac0 = hmac.HMAC(intKey, hashes.SHA256(), backend=default_backend())

    cipher1 = Cipher(algorithms.AES(key), modes.CBC(iv1), backend=default_backend())
    encryptor1 = cipher1.encryptor()

    c_iv_key = encryptor1.update(iv0 + intKey) + encryptor1.finalize()

    hmac1 = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    hmac1.update(c_iv_key)

    fOut.write(bytes("AES", "utf8"))

    fOut.write(b"\x02")

    fOut.write(b"\x00")

    cby = "OpenFileEncryptor" + version

    fOut.write(b"\x00" + bytes([1 + len("CREATED_BY" + cby)]))

    fOut.write(bytes("CREATED_BY", "utf8") + b"\x00" + bytes(cby, "utf8"))

    fOut.write(b"\x00\x80")

    for i in range(128):
        fOut.write(b"\x00")

    fOut.write(b"\x00\x00")

    fOut.write(iv1)

    fOut.write(c_iv_key)

    fOut.write(hmac1.finalize())

    while True:
        fdata = fIn.read(bufferSize)

        bytesRead = len(fdata)

        if bytesRead < bufferSize:
            fs16 = bytes([bytesRead % AESBlockSize])
            if bytesRead % AESBlockSize == 0:
                padLen = 0
            else:
                padLen = 16 - bytesRead % AESBlockSize
            fdata += bytes([padLen]) * padLen
            cText = encryptor0.update(fdata) + encryptor0.finalize()
            hmac0.update(cText)
            fOut.write(cText)
            break
        else:
            cText = encryptor0.update(fdata)
            hmac0.update(cText)
            fOut.write(cText)

    fOut.write(fs16)

    fOut.write(hmac0.finalize())

def decryptFile(infile, outfile, passw, bufferSize=bufferSizeDef):
    try:
        with open(infile, "rb") as fIn:
            if path.isfile(outfile):
                if path.samefile(infile, outfile):
                    raise ValueError("Input and output files are the same.")
            try:
                with open(outfile, "wb") as fOut:
                    try:
                        decryptStream(fIn, fOut, passw, bufferSize)
                    except ValueError as exd:
                        raise ValueError(str(exd))

            except IOError:
                raise ValueError("Unable to write output file.")
            except ValueError as exd:
                remove(outfile)
                raise ValueError(str(exd))

    except IOError:
        raise ValueError("Unable to read input file.")

def decryptStream(fIn, fOut, passw, bufferSize=bufferSizeDef, inputLength=None):
    if inputLength is not None:
        warnings.warn(
            "inputLength parameter is no longer used, and might be removed in a future version",
            DeprecationWarning,
            stacklevel=2,
        )
    if bufferSize % AESBlockSize != 0:
        raise ValueError("Buffer size must be a multiple of AES block size")

    if len(passw) > maxPassLen:
        raise ValueError("Password is too long.")

    if not hasattr(fIn, "peek"):
        fIn = io.BufferedReader(getBufferableFileobj(fIn), bufferSize)

    fdata = fIn.read(3)
    if fdata != b"AES":
        raise ValueError("File is corrupted or not an AES Crypt (or pyAesCrypt) file.")

    fdata = fIn.read(1)
    if len(fdata) != 1:
        raise ValueError("File is corrupted.")

    if fdata != b"\x02":
        raise ValueError(
            "pyAesCrypt is only compatible with version "
            "2 of the AES Crypt file format."
        )

    fIn.read(1)

    while True:
        fdata = fIn.read(2)
        if len(fdata) != 2:
            raise ValueError("File is corrupted.")
        if fdata == b"\x00\x00":
            break
        fIn.read(int.from_bytes(fdata, byteorder="big"))

    iv1 = fIn.read(16)
    if len(iv1) != 16:
        raise ValueError("File is corrupted.")

    key = stretch(passw, iv1)

    c_iv_key = fIn.read(48)
    if len(c_iv_key) != 48:
        raise ValueError("File is corrupted.")

    hmac1 = fIn.read(32)
    if len(hmac1) != 32:
        raise ValueError("File is corrupted.")

    hmac1Act = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    hmac1Act.update(c_iv_key)

    if hmac1 != hmac1Act.finalize():
        raise ValueError("Wrong password (or file is corrupted).")

    cipher1 = Cipher(algorithms.AES(key), modes.CBC(iv1), backend=default_backend())
    decryptor1 = cipher1.decryptor()

    iv_key = decryptor1.update(c_iv_key) + decryptor1.finalize()

    iv0 = iv_key[:16]
    intKey = iv_key[16:]

    cipher0 = Cipher(algorithms.AES(intKey), modes.CBC(iv0), backend=default_backend())
    decryptor0 = cipher0.decryptor()

    hmac0Act = hmac.HMAC(intKey, hashes.SHA256(), backend=default_backend())

    last_block_reached = False
    while not last_block_reached:
        cText = fIn.read(bufferSize)
        if len(fIn.peek(32 + 1)) < 32 + 1:
            last_block_reached = True
            cText += fIn.read()
            fs16 = cText[-32 - 1]
            hmac0 = cText[-32:]
            cText = cText[: -32 - 1]

        hmac0Act.update(cText)
        pText = decryptor0.update(cText)

        if last_block_reached:
            toremove = (16 - fs16) % 16
            if toremove:
                pText = pText[:-toremove]

        fOut.write(pText)

    if hmac0 != hmac0Act.finalize():
        raise ValueError("Bad HMAC (file is corrupted).")

class BufferableFileobj:
    def __init__(self, fileobj):
        self.__fileobj = fileobj
        self.closed = False

    def readable(self):
        return True

    def read(self, n = -1):
        return self.__fileobj.read(n)

    def readinto(self, b):
        rbuf = self.read(len(b))
        n = len(rbuf)
        b[0:n] = rbuf
        return n

def getBufferableFileobj(fileobj):
    noattr = object()
    for attr in ('readable','readinto','closed'):
        if getattr(fileobj, attr, noattr) == noattr:
            return BufferableFileobj(fileobj)
    return fileobj
