#!/bin/bash


pyinstaller --onefile -w pinger.py
mkdir -p dist/config
cp -rv config/* dist/config
