# find-my-secrets

Do you know where, on your development machine, you have credentials stored? SSH, Chef, AWS, what else did you forget? This small script tells you.

## Getting started

```
git clone https://github.com/abesto/find-my-secrets
cd find-my-secrets
python main.py
```

The output will be something like this:

```
                      SSH private key in /Users/abesto/.ssh/abesto
                      SSH private key in /Users/abesto/.ssh/elasticbeanstalk-user
                      SSH private key in /Users/abesto/.ssh/id_boot2docker
                      SSH private key in /Users/abesto/.ssh/id_rsa
           Chef validator private key in /Users/abesto/.chef/validator.pem
Potential Chef encrypted data bag key in /Users/abesto/.chef/encrypted_data_bag_secret
```

## Detection rules

`find-my-secrets` comes equipped with three sets of detection rules:

 * [`default_rules`](default_rules.py): Very specific, runs quickly, but finds only types of secrets it explicitly knows about
 * [`scan_home`](scan_home.py): Scans your `$HOME` for filenames and content hinting to secrets. Very slow, but comprehensive
 * [`scan_full_fs`](scan_full_fs.py): Scans the full file-system for filenames and content hinting to secrets. Very slow, but comprehensive
 
 To use a specific rule-set:
 
 ```
 python main.py -r scan_home
 ```

You can define custom rule-sets by creating a new Python module following the API of the provided rule-sets.
