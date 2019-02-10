# 2.1.0
* Disable module 4 and STRIPE (not used)
* Display TOU before showing the list of modules
* Add `has_tou` flag in `area_app_user`

# 2.0.0
* Release module 3

# 1.2.0
* Change hardcoded copyright year to be dynamic

# 1.1.0
* Add `docs/` folder
* Add `CHANGELOG.md` and `VERSION.md` to track changes and have some sense of versioning
* Add my local dev instructions (so far)
* Update paramiko due to vulnerability to 2.0.8
* Update numpy 1.8.0rc1 to 1.8.0 since 1.8.0rc1 no longer exists
* Update scipy 0.13.0b1 to 0.13.0 since 0.13.0b1 no longer exists
* Update pyOpenSSL 0.13.1 to 0.14 since anything older throws `OpenSSL/crypto/crl.c::23: error: static declaration of 'X509_REVOKED_dup' follows non-static declaration`
* Remove pyobjc libraries since they will not build on Ubuntu

# 1.0.0
- initial version from vadim
