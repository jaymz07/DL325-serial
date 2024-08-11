# DL325-serial
Simple script showing serial control of a Newport DL325 translation stage.

The default software shipping with the translation stage does not allow for easy integration with many single board computers. One of the reasons for this is the default python interface needs to interact with a Windows DLL file with some .NET references.

By treating the device as a simple USB to serial converter, we can bypass the need
for any .NET dependence. This module only requires pyserial.
