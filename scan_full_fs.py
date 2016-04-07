def rules(build):
    build.reporter = build.FastReporter
    return [
        build.Grep("/", "AKIA\|PRIVATE KEY", "Potentially sensitive information"),
        build.Find("/", [
            "*.key", 
            "*.pem",
            "*id_rsa*",
            "*encrypted_data_bag*",
            "*credential*",
            "*history*",
            "*token*",
            "*rc"
        ] , "Potentially sensitive information"),
    ]
