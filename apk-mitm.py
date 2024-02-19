import os
import re
import subprocess
import shutil

def ensure_raw_directory_exists(decompiled_apk_dir):
    raw_dir = os.path.join(decompiled_apk_dir, 'res', 'raw')
    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir)
    print(f"Ensured that {raw_dir} exists.")

def add_custom_certificate(apk_name, certificate_path):
    decompiled_apk_dir = f"{apk_name}_decompiled"
    ensure_raw_directory_exists(decompiled_apk_dir)
    dest_certificate_path = os.path.join(decompiled_apk_dir, 'res', 'raw', 'cert.pem')
    
    if not os.path.isfile(certificate_path):
        print(f"Certificate file '{certificate_path}' not found.")
        return

    shutil.copy(certificate_path, dest_certificate_path)
    print(f"Certificate copied to {dest_certificate_path}.")

    network_security_config = os.path.join(decompiled_apk_dir, 'res', 'xml', 'network_security_config.xml')
    try:
        with open(network_security_config, "a") as file:
            file.write(f"\n    <certificates src=\"@raw/cert\"/>\n")
        print("Custom certificate reference added to network_security_config.xml.")
    except Exception as e:
        print(f"Error modifying network_security_config.xml: {e}")

def remove_decompiled_directory(apk_name):
    decompiled_dir = f"{apk_name}_decompiled"
    if os.path.exists(decompiled_dir):  # Verifica se o diretório existe
        try:
            shutil.rmtree(decompiled_dir)
            print(f"Removed directory: {decompiled_dir}")
        except OSError as e:
            print(f"Error removing directory {decompiled_dir}: {e.strerror}")
    else:
        print(f"Directory does not exist, no need to remove: {decompiled_dir}")


def remove_files_with_problematic_attributes(decompiled_apk_dir):
    animation_dirs = [f"{decompiled_apk_dir}/res/anim-v33/"]
    problematic_attributes = [
        'android:fromExtendBottom',
        'android:fromExtendLeft',
        'android:fromExtendRight',
        'android:fromExtendTop',
        'android:toExtendBottom',
        'android:toExtendLeft',
        'android:toExtendRight',
        'android:toExtendTop'
    ]
    attr_regex = '|'.join([re.escape(attr) for attr in problematic_attributes])
    
    for anim_dir in animation_dirs:
        if os.path.exists(anim_dir):
            for file in os.listdir(anim_dir):
                if file.endswith(".xml"):
                    file_path = os.path.join(anim_dir, file)
                    with open(file_path, "r") as f:
                        content = f.read()
                        # Check if any problematic attribute is in the file
                        if re.search(attr_regex, content):
                            os.remove(file_path)  # Remove the file
                            print(f"Removed {file_path} due to problematic attributes.")


def decompile_apk(apk_name):
    output_dir = f"{apk_name}_decompiled"
    try:
        subprocess.run(["apktool", "d", f"{apk_name}.apk", "-o", output_dir], check=True)
        print(f"APK decompiled successfully to {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error decompiling APK: {e}")

def recompile_and_sign_apk(apk_name, keystore="debug.keystore", keystore_pass="android"):
    decompiled_apk_dir = f"{apk_name}_decompiled"
    output_apk = f"{apk_name}_modified.apk"
    
    # Recompilar o APK
    try:
        subprocess.run(["apktool", "b", decompiled_apk_dir, "-o", output_apk], check=True)
        print(f"APK recompiled successfully to {output_apk}")
    except subprocess.CalledProcessError as e:
        print(f"Error recompiling APK: {e}")
        return  # Encerra a função se a recompilação falhar

    # Verifica se o keystore existe
    if not os.path.isfile(keystore):
        print(f"Keystore file '{keystore}' not found.")
        return  # Encerra a função se o keystore não existir

    # Caminho completo para o apksigner altere para seu path caso tenha algum problema
    apksigner_path = "apksigner"
    
    # Assinar o APK
    try:
        subprocess.run([
            apksigner_path, "sign", "--ks", keystore, "--ks-pass", f"pass:{keystore_pass}", output_apk
        ], check=True)
        print("APK signed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error signing APK: {e}")



# Script execution
apk_name = "fafa"  # Nome do seu arquivo APK sem a extensão
certificate_path = "cert.pem"  # Atualize com o caminho correto para o certificado

remove_decompiled_directory(apk_name)
decompile_apk(apk_name)
remove_files_with_problematic_attributes(f"{apk_name}_decompiled")
add_custom_certificate(apk_name, certificate_path)
recompile_and_sign_apk(apk_name)
