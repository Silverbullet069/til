# Limit Sudo Timeout

<!-- tl;dr starts -->

By default, once a command running with `sudo` privillege, that terminal session stays `sudo` all the time. According to CIS standard it's best to reduce sudo timeout to `0`.

<!-- tl;dr ends -->

```sh
echo "Defaults timestamp_timeout = 0" | sudo tee -a "/etc/sudoers.d/defaults_timestamp_timeout"
sudo chmod 0440 "/etc/sudoers.d/defaults_timestamp_timeout"
sudo chown root:root "/etc/sudoers.d/defaults_timestamp_timeout"
sudo visudo -c
```
