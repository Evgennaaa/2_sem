#!/bin/bash

# Получение имени пользователя
USERNAME=$(whoami)

# Вывод имени пользователя
echo "Привет, ${USERNAME}!"#!/usr/bin/env bash 

# Вывод текущего времени
current_time=$(date +"%T")

echo "Текущее время: $current_time"

# Вывод текущей даты и времени
current_date=$(date +"%Y-%m-%d")
echo "Текущая дата: $current_date"
