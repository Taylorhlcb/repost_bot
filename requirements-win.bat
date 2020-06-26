:: View requirements-win-README.txt for instructions for running the project on windows
echo off
echo "// Installing and setting up the virtual environment"
pip install virtualenvwrapper-win
if exist "%USERPROFILE%\Envs\auth_bot" (
echo "Duplicate Environment, removing old env"
rmdir %USERPROFILE%\Envs\auth_bot /Q /S
)
mkvirtualenv -r requirements-win-pip auth_bot
echo "Setup Complete"
pause