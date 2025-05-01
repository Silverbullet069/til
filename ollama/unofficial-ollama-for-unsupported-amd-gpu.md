# Unofficial Ollama for unsupported AMD GPU

<!-- tl;dr starts -->

I would like to run [arcee-ai/Arcee-Vylinh-GGUF](https://huggingface.co/arcee-ai/Arcee-VyLinh-GGUF) on my laptop and my older brother's PC to be able to chat with my local data by RAG-ing models. If you're not a masochist, use [Google NotebookLM](https://notebooklm.google.com) instead.

<!-- tl;dr ends -->

## My machine

**TL;DR**: I've made it worked, but it's unstable. Desktop can crash at anytime. It might work for you flawlessly, but not for me. I considered I've failed this task, miserably. 3 days for a simple lesson - _Don't work on things that are over your head and give you little benefit_.

Use this snippet from my `docker-compose.yml`:

```yml
services:
  # Cre: https://hub.docker.com/r/ollama/ollama
  ollama:
    image: ollama/ollama:rocm # ollama/ollama (CPU only)
    container_name: ollama
    restart: unless-stopped
    networks:
      - llmnet
    devices:
      - /dev/kfd
      - /dev/dri
    security_opt:
      - "seccomp:unconfined"
    volumes:
      - ./ollama:/root/.ollama
    ports:
      - 11434:11434
    environment:
      # Only works if you have more than 2GB of VRAM allocated from UMA Frame Buffer in UEFI/BIOS
      - HSA_OVERRIDE_GFX_VERSION=9.0.0
    # don't know when to start, usually right after the start of container so it's reliable enough
    post_start:
      - command: sh -c "/usr/bin/ollama run --keepalive 1h hf.co/arcee-ai/Arcee-VyLinh-GGUF"
```

---

- Product: [Lenovo Yoga Slim 7 2020 AMD Ryzen 7 4800H](https://psref.lenovo.com/syspool/Sys/PDF/datasheet/Yoga%20Slim%207%20Pro%2014ARH5_datasheet_EN.pdf)
- GPU type: APU (CPU AMD Ryzen 7 4800H + iGPU AMD Radeon Vega 8)
- GPU architecture: `gfx90c:xnack+` (check by running `rocminfo | grep 'Name'` on Linux). My speculation is **maybe this is the cause that crash my system**. It's not `gfx90c` or `gfx90c:xnack-`, which are more popular.
- Ollama: Docker, ROCm-supported: `ollama/ollama:rocm`.

Here's what I've found:

- [Somebody with Ryzen 7 5800H APU](https://github.com/ROCm/rocBLAS/issues/1398#issuecomment-1984229135) can run ROCm by overriding HSA version: `export HSA_OVERRIDE_GFX_VERSION=9.0.0`. I don't know about his installation method or his GPU architecture so [I had to ask about him](https://github.com/ROCm/rocBLAS/issues/1398#issuecomment-2544644844).

- According to [langyuxf on ROCm#1743](https://github.com/ROCm/ROCm/issues/1743#issuecomment-1156009899) `gfx900` shares the same ISA architecture with `gfx90c` so that's explained why `export HSA_OVERRIDE_GFX_VERSION=9.0.0` worked with some people. But people with edge case like me is rarer.

- [AMD ROCm 6.3.0 Docs "System requirements (Linux)"](https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.3.0/reference/system-requirements.html) stated that `gfx900` architecture isn't officially supported. What Official Ollama used is a set of ROCmlib built by 3rd-party.

- [langyuxf on ROCm#1743](https://github.com/ROCm/ROCm/issues/1743#issuecomment-1150974181) also recommended that video memory should be `>=2GB`. I've only set to `1GB` since that's the minimum size to pass Ollama ROCm GPU detector. If not allocated enough Ollama will silently use 100% CPU without informing any warnings or errors about the lack of memory. I've changed my `UMA Frame Buffer` size to `4GB` and IT WORKED! Sadly Ollama crashed too frequently, I can't use this approach.

- Finally, haol666 asked for `gfx90c` support on [ollama-for-amd#33](https://github.com/likelovewant/ollama-for-amd/issues/33). I should have given up the moment I read this post, but I chose to find. I've managed to share[ my digging rabbit hole experience](https://github.com/likelovewant/ollama-for-amd/issues/33#issuecomment-2545806096), and asked the repository's owner about how to build a ROCmlib specifically for Linux. You could try to if you want, but this guy isn't someone who can teach, so good luck: https://github.com/likelovewant/ollama-for-amd/issues/33#issuecomment-2545971894

## My older brother's machine - Prefer

Download [Ollama-For-AMD-Installer.exe](https://github.com/ByronLeeeee/Ollama-For-AMD-Installer/releases/download/Releases/Ollama-For-AMD-Installer.exe), install Ollama, choose `gfx1032` and replace library.

---

My brother has bough an [AMD Radeon RX6600](https://www.amd.com/en/products/graphics/desktops/radeon/6000-series/amd-radeon-rx-6600.html) before. Fortunately enough, RX 6600 that used `gfx1032` architecture is the first product to be supported by **ROCm runtime**, but not by **HIP SDK**. [ollama#2869](https://github.com/ollama/ollama/issues/2869#issuecomment-2009112162) has also mentioned about `gfx1032` is not supported.

I have to result to [likelovewant/ROCmLibs-for-gfx1103-AMD780M-APU](https://github.com/likelovewant/ROCmLibs-for-gfx1103-AMD780M-APU/releases) to install library replacements for current ROCm: [`rocm.gfx1032.for.hip.sdk.6.1.2.7z`](https://github.com/likelovewant/ROCmLibs-for-gfx1103-AMD780M-APU/releases/download/v0.6.1.2/rocm.gfx1032.for.hip.sdk.6.1.2.7z).

However, the installation instruction is horrendous. I've re-read many times and still can't understand what to put where. Luckily, ByronLeeeee create [Ollama-For-AMD-Installer](https://github.com/ByronLeeeee/Ollama-For-AMD-Installer) that simplified the process. Just clone the repository, create Python virtual environment, install Python dependencies and run `ollama_installer.py`.

Going back-and-forth from my room to my older brother's room to manually open the machine is tedious. I am trying to setup `Shutdown Start Remote` again to trigger Wake on LAN on his machine but it's still unreliable.

That concludes my 3 days investigation. Hopefully I will not repeat the same mistakes ever. again.
