# Android APK MITM Preparation Script

Este script facilita a realização de ataques Man-In-The-Middle (MITM) em aplicativos Android, permitindo a inserção de um certificado personalizado no APK desejado. Ele automatiza o processo de descompilação do APK, adição do certificado, e recompilação e assinatura do APK modificado.

## Pré-requisitos

Antes de usar este script, você precisa instalar os seguintes softwares:

- **JDK (Java Development Kit):** Necessário para assinar o APK. Disponível para download em: [Oracle JDK](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html) ou [OpenJDK](https://openjdk.java.net/install/).
- **Apktool:** Para descompilar e recompilar APKs. Faça o download e leia as instruções de instalação em [iBotPeaches/Apktool](https://github.com/iBotPeaches/Apktool).
- **Android Build Tools:** Contém o `apksigner` para assinar o APK. Instale através do Android SDK Manager ou encontre as instruções em [Android Developers](https://developer.android.com/studio/releases/build-tools).

## Configuração

1. **Clone o repositório:**
   ```bash
   git clone <URL do repositório>
   ```

Certifique-se de que todos os pré-requisitos estejam instalados e configurados corretamente.

## Geração de Certificado e Keystore
Para gerar um certificado .pem e um keystore, siga os passos abaixo:

Gerar um novo keystore (se necessário):
```bash
keytool -genkey -v -keystore meu-keystore.keystore -alias meu_alias -keyalg RSA -keysize 2048 -validity 10000
```


## Extrair o certificado do keystore:
```bash
keytool -export -keystore meu-keystore.keystore -alias meu_alias -file cert.pem
```


Certifique-se de substituir meu-keystore.keystore, meu_alias, e cert.pem pelos nomes desejados.

## Uso
Certifique-se de que o APK, o certificado .pem, e o keystore estejam no mesmo diretório que o script.
Modifique as variáveis apk_name, certificate_path, keystore, e keystore_pass no script conforme necessário.

## Execute o script:
```bash
python nome_do_script.py
```


## Importante
Este script é destinado apenas para fins educacionais e de testes de segurança com permissão.
A recompilação de APKs pode não funcionar para todos os aplicativos devido a proteções específicas ou características do aplicativo.
