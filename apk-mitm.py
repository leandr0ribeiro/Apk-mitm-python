import os
import re
import subprocess
import shutil

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    print(f"Ensured that {directory_path} exists.")

def add_custom_certificate(apk_name, certificate_path):
    decompiled_apk_dir = f"{apk_name}_decompiled"
    res_raw_dir = os.path.join(decompiled_apk_dir, 'res', 'raw')
    ensure_directory_exists(res_raw_dir)
    
    # Use a unique name for the certificate to avoid conflicts
    dest_certificate_path = os.path.join(res_raw_dir, 'custom_cert.pem')
    
    if not os.path.isfile(certificate_path):
        print(f"Certificate file '{certificate_path}' not found.")
        return

    shutil.copy(certificate_path, dest_certificate_path)
    print(f"Certificate copied to {dest_certificate_path}.")

    network_security_config = os.path.join(decompiled_apk_dir, 'res', 'xml', 'network_security_config.xml')
    if not os.path.isfile(network_security_config):
        print("network_security_config.xml not found. Ensure your APK includes it if you need custom trust anchors.")
        return
    
    try:
        with open(network_security_config, "r") as file:
            content = file.readlines()

        end_index = next((i for i, line in enumerate(content) if '</base-config>' in line or '</network-security-config>' in line), None)

        if end_index is not None:
            cert_tag = '    <trust-anchors>\n        <certificates src="@raw/custom_cert" />\n    </trust-anchors>\n'
            content.insert(end_index, cert_tag)

            with open(network_security_config, "w") as file:
                file.writelines(content)

            print("Custom certificate reference added to network_security_config.xml.")
    except Exception as e:
        print(f"Error modifying network_security_config.xml: {e}")

def remove_decompiled_directory(decompiled_apk_dir):
    if os.path.exists(decompiled_apk_dir):
        try:
            shutil.rmtree(decompiled_apk_dir)
            print(f"Removed directory: {decompiled_apk_dir}")
        except OSError as e:
            print(f"Error removing directory {decompiled_apk_dir}: {e.strerror}")
    else:
        print(f"Directory does not exist, no need to remove: {decompiled_apk_dir}")

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
    
    try:
        subprocess.run(["apktool", "b", decompiled_apk_dir, "-o", output_apk], check=True)
        print(f"APK recompiled successfully to {output_apk}")
    except subprocess.CalledProcessError as e:
        print(f"Error recompiling APK: {e}")
        return

    if not os.path.isfile(keystore):
        print(f"Keystore file '{keystore}' not found.")
        return

    apksigner_path = "/path/to/your/apksigner"  # Update this path to your apksigner location
    
    try:
        subprocess.run([
            apksigner_path, "sign", "--ks", keystore, "--ks-pass", f"pass:{keystore_pass}", output_apk
        ], check=True)
        print("APK signed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error signing APK: {e}")

# Example usage
apk_name = "YourAppName" #dont put .apk
certificate_path = "path/to/your/cert.pem"  # Update this path to your certificate location

remove_decompiled_directory(f"{apk_name}_decompiled")
decompile_apk(apk_name)
add_custom_certificate(apk_name, certificate_path)
recompile_and_sign_apk(apk_name)
