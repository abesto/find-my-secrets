def rules(build):
    return [
        build.Find("/", [
            "*.key", 
            "*.pem",
            "*id_rsa*",
            "*encrypted_data_bag*",
            "*credential*",
            "*history*",
            "*token*",
            "*rc"
        ] , "Potentially sensitive information")
    ]
