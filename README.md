# wifi-radar

Plots strength of WiFi AP signal across time.

Useful for directional finding

![](https://github.com/nemanjan00/wifi-radar/blob/master/screenshot/example.png?raw=true)

## Table of contents

<!-- vim-markdown-toc GitLab -->

* [Usage](#usage)
* [How does it work?](#how-does-it-work)
* [Authors](#authors)

<!-- vim-markdown-toc -->

## Usage

```bash
sudo python ./main.py --interface wlan0mon --ssid OpenAP
```

## How does it work?

It continously sends Probe Requests to AP and measures response power

## Authors

* [nemanjan00](https://github.com/nemanjan00)
