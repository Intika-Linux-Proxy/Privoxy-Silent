# Privoxy-Anonyme v3.0.28
Patched Privoxy Version To Make It Less Detectable And More Silent 

Built with 
```
./configure --with-user=daemon --with-group=daemon --disable-image-blocking --disable-client-tags --enable-graceful-termination=no --enable-external-filters=no --enable-editor=no --enable-trust-files=no --enable-toggle=no --enable-fuzz=no --disable-force
```

And 
```
Patch0:		privoxy-3.0.21-mga-mdv-missing-user.filter.patch
#(cjw) add a "address-family-preference" option that allows disabling IPv6 DNS lookups, forcing outgoing HTTP requests to be IPv4
Patch1:		privoxy-3.0.21-mga-address-family-preference.patch
#(cjw) from debian: don't translate documentation to locale-dependent 8-bit ascii
Patch2:		privoxy-3.0.21-mga-deb-8bit_manual.patch
#(cjw) documentation and default configuration changes and cleanups for mageia
Patch3:		privoxy-3.0.21-mga-mageia-specific-config.patch
Patch4:		privoxy-3.0.28-mga-intika-config-page.patch
Patch5:		privoxy-3.0.28-mga-intika-anonimyzer.patch
Patch6:		privoxy-3.0.28-mga-intika-shutup-no-answer.patch
```
