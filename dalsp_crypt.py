import gzip
import os
import subprocess


def decryptZIP(param_1, param_2):
    param_1[1] = 0x1f
    param_1[2] = 0x8b
    uVar3 = 0x14
    if (param_2 - 3) < int(str(0x15)):
        uVar3 = param_2 - 3
    if 0 < uVar3:
        iVar4 = 2
        iVar1 = uVar3 + 2
    while True:
        uVar2 = uVar3 % 0x2d
        uVar3 = param_1[iVar4 + 1] + uVar2
        param_1[iVar4 + 1] = uVar2 ^ param_1[iVar4 + 1]
        iVar4 = iVar4 + 1
        if not (iVar4 < iVar1):
            break
    data = gzip.decompress(bytes(param_1[1:]))
    return data, 1


def decryptToPcm(pcVar5, iVar4):
    while pcVar5[:3] == [0xFB, 0x1B, 0x9D]:
        bVar2 = pcVar5[3]
        iVar10 = iVar4 + -4
        iVar6 = iVar10
        pbVar9 = pcVar5[4:]
        if 4 < iVar4:
            i = 0
            while True:
                iVar6 = iVar6 + -1
                pbVar9[i] = pbVar9[i] ^ bVar2
                i = i + 1
                if not (iVar6 != 0):
                    break
        pcVar5 = pbVar9
        iVar4 = len(pcVar5)
    return bytes(pcVar5), 1


def decrypt_assets(data):
    param_1 = list(data)
    param_2 = len(param_1)
    if param_1[:2] == [0xf8, 0x8b]:
        if param_1[2] in [0x2d, 0x3d]:
            data, retval = decryptZIP(param_1, param_2)
        else:
            retval = -1
    elif param_1[:3] == [0xFB, 0x1B, 0x9D]:
        data, retval = decryptToPcm(param_1, param_2)
    else:
        retval = 0
    return data, retval


def write(path, content):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    open(path, 'wb').write(content)


def unpack_PVR(filepath, options):
    if options.unpackPVR and os.path.splitext(filepath)[1] == ".pvr":
        filename = os.path.basename(filepath)
        fileout = os.path.splitext(filepath)[0] + ".png"
        plistout = os.path.join(options.output_path, "info.plist")
        with open(os.devnull, 'w') as FNULL:
            if options.verbose:
                print("Unpacking PVR: ", filename)
            command = ["texturepacker", filepath,
                       "--sheet", fileout, "--data", plistout]
            process = subprocess.Popen(
                command, stdout=FNULL, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
        if options.verbose:
            string = stderr.decode("utf-8")
            if string == "":
                print("Done. No error found.")
                if not options.keepPVR:
                    os.remove(filepath)
            else:
                print("There's an error, need to manually unpack")
                print(string)
            print()


def decrypt_file(path, relpath, name, output_path, options):
    fileexist = os.path.join(output_path, relpath, name)
    if not options.overwrite:
        if os.path.isfile(fileexist):
            if options.verbose:
                print(name, "already exists at destination, skipping...")
            return
    with open(path, "rb") as file:
        data = file.read()
        if options.verbose:
            print("Reading:", os.path.join(relpath, name))
        buff, retval = decrypt_assets(data)
        while buff[:3] == b"MNG":
            buff = buff[7:]
        if buff[:3] == b"PVR":
            name = os.path.splitext(name)[0] + ".pvr"
        if options.verbose:
            debug_dict = {
                -1: "Wrong decryption method, will not write to destination",
                0: "File is not encrypted, write to destination anyway",
                1: "Decrypted",
            }
            print(debug_dict[retval])
            print()
        if retval != -1:
            filepath = os.path.join(output_path, relpath, name)
            write(filepath, buff)
            unpack_PVR(filepath, options)


def decrypt_folder(options):
    input_path = options.input_path
    output_path = options.output_path
    for root, dirs, files in os.walk(input_path):
        for name in files:
            relpath = os.path.relpath(root, input_path)
            path = os.path.join(root, name)
            decrypt_file(path, relpath, name, output_path, options)


def decrypt_single_file(options):
    input_path = options.input_path
    output_path = options.output_path
    relpath = ""
    name = os.path.basename(input_path)
    decrypt_file(input_path, relpath, name, output_path, options)


if __name__ == "__main__":
    class options:
        input_path = 'tmp/cap2.mp4'
        output_path = 'tmp_dec/'
        file_mode = False
        verbose = True


    decrypt_single_file(options)
