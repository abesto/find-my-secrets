def rules(build):
    return [
        # SSH
        build.FilesContain("~/.ssh/**", "PRIVATE KEY", "SSH private key"),
        # Chef
        build.FilesContain("~/.chef/**", "PRIVATE KEY", "Chef validator private key"),
        build.FilesExist("~/.chef/*encrypted*", "Potential Chef encrypted data bag key"),
        # AWS unified secrets
        build.FilesExist("~/.aws/credentials*", "Unified AWS credentials"),
        # Old-style EC2 secrets
        build.FilesExist("~/.ec2/aws-credential", "AWS credentials"),
        build.FilesExist("~/.ec2/cert-amazon.pem", "AWS IAM certificate"),
        build.FilesExist("~/.ec2/pk-amazon.pem", "AWS IAM private key"),
        # Old-style S3 secrets
        build.FilesExist("~/.s3cmd", "AWS S3 configuration"),
        # Basic auth for PyPI servers
        build.FilesContain("~/.pip/pip.conf", "extra-index-url.*https?://.*:", "Basic auth password to a PyPI server"),
        # Gradle
        build.FilesContain("~/.gradle/gradle.properties", "Password", "Package index credentials for Gradle"),
        # Docker
        build.FilesContain("~/.docker/config.json", "auth", "Docker registry credentials"),
        # LastPass
        build.FilesExist("~/.lpass/session_privatekey", "LastPass CLI session"),
        # Vault
        build.FilesExist("~/.vault_token", "HashiCorp Vault token")
    ]
