#!/bin/sh

#remove client stuff
rm -rf ~/Library/Caches/com.spotify.client
rm -rf ~/Library/Application\ Support/Spotify/
rm -rf /Applications/Spotify.app/
rm -rf ~/Downloads/Install\ Spotify.app/

#remove Flash cookies (FB)
rm -rf ~/Library/Preferences/Macromedia/Flash\ Player/#SharedObjects/*
rm -rf ~/Library/Preferences/Macromedia/Flash\ Player/macromedia.com/support/flashplayer/sys/*
