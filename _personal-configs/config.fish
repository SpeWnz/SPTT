# wget https://raw.githubusercontent.com/SpeWnz/SPTT/refs/heads/main/_personal-configs/config.fish -O ~/.config/fish/config.fish

if status is-interactive
    # uncomment this if you get the weird 5u/ou output
    #set -Ua fish_features no-keyboard-protocols


    alias ll='ls -al'
    alias llh='ls -lah'
    alias python-init-venv='echo "Initializing Python venv..."; python3 -m venv .venv; source .venv/bin/activate.fish'
    set SPTT ~/Documents/github-tools/SPTT/
    set NOFI ~/Documents/github-tools/NO-FI-Zone/
    set ZHOR /usr/lib/python3/dist-packages/ZHOR_Modules/
end
