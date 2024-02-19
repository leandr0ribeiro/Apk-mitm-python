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
   git clone <URL do repositório> ```
