@if "%SCM_TRACE_LEVEL%" NEQ "4" @echo off
:: ----------------------
:: KUDU Deployment Script
:: Version: 1.0.8
:: ----------------------
:: Prerequisites
:: -------------
:: Verify node.js installed
where node 2>nul >nul
IF %ERRORLEVEL% NEQ 0 (
  echo Missing node.js executable, please install node.js, if already installed make sure it can be reached from current environment.
  goto error
)
:: VARIABLES
echo "ATTENTION"
echo "USER MUST CHECK/SET THESE VARIABLES:"
SET PYTHON_EXE=%SYSTEMDRIVE%\home\python354x64\python.exe
echo "Installed python extension installed here:"
echo %PYTHON_EXE%

:: Setup
:: -----
setlocal enabledelayedexpansion
SET ARTIFACTS=%~dp0%..\artifacts
IF NOT DEFINED DEPLOYMENT_SOURCE (
  SET DEPLOYMENT_SOURCE=%~dp0%.
)
IF NOT DEFINED DEPLOYMENT_TARGET (
  SET DEPLOYMENT_TARGET=%ARTIFACTS%\wwwroot
)
IF NOT DEFINED NEXT_MANIFEST_PATH (
  SET NEXT_MANIFEST_PATH=%ARTIFACTS%\manifest
  IF NOT DEFINED PREVIOUS_MANIFEST_PATH (
    SET PREVIOUS_MANIFEST_PATH=%ARTIFACTS%\manifest
  )
)
IF NOT DEFINED KUDU_SYNC_CMD (
  :: Install kudu sync
  echo Installing Kudu Sync
  call npm install kudusync -g --silent
  IF !ERRORLEVEL! NEQ 0 goto error
  :: Locally just running "kuduSync" would also work
  SET KUDU_SYNC_CMD=%appdata%\npm\kuduSync.cmd
)
goto Deployment

:: Utility Functions
:: -----------------
:InstallCNTK
pushd "%DEPLOYMENT_TARGET%"
echo "Installing CNTK; Extracting archive"

rm -rf cntk
unzip cntk.zip
echo "Extracted CNTK ..."
popd  


echo "Setting CNTK PATH"
set CNTK_HOME=%DEPLOYMENT_TARGET%\cntk\cntk
SET CNTK_WHEEL=cntk-2.0rc1-cp35-cp35m-win_amd64.whl
set PATH=%CNTK_HOME%;%PATH%
pushd "%DEPLOYMENT_TARGET%\Wheels"

%PYTHON_EXE% -m pip install %CNTK_WHEEL%
echo "CNTK Version:"
%PYTHON_EXE% -c "import cntk;print(cntk.__version__)"
popd


goto :EOF

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:Deployment
echo Handling python deployment.
:: 1. KuduSync
IF /I "%IN_PLACE_DEPLOYMENT%" NEQ "1" (
  call :ExecuteCmd "%KUDU_SYNC_CMD%" -v 50 -f "%DEPLOYMENT_SOURCE%" -t "%DEPLOYMENT_TARGET%" -n "%NEXT_MANIFEST_PATH%" -p "%PREVIOUS_MANIFEST_PATH%" -i ".git;.hg;.deployment;deploy.cmd"
  IF !ERRORLEVEL! NEQ 0 goto error
)
IF NOT EXIST "%DEPLOYMENT_TARGET%\requirements.txt" goto postPython
IF EXIST "%DEPLOYMENT_TARGET%\.skipPythonDeployment" goto postPython
echo Detected requirements.txt.  You can skip Python specific steps with a .skipPythonDeployment file.
pushd "%DEPLOYMENT_TARGET%"
:: 3. Setup python
echo "Configuring pip"
curl https://bootstrap.pypa.io/get-pip.py | %PYTHON_EXE%

:: 4. Install packages
echo Pip install requirements.
echo "Installing requirements"  
%PYTHON_EXE% -m pip install -r requirements.txt
IF !ERRORLEVEL! NEQ 0 goto error
:: 5. Install CNTK
IF EXIST "%DEPLOYMENT_TARGET%\cntk" (
  echo "CNTK already installed"
) ELSE (
  call :InstallCNTK
)
:postPython
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
goto end

:: Execute command routine that will echo out when error
:ExecuteCmd
setlocal
set _CMD_=%*
call %_CMD_%
if "%ERRORLEVEL%" NEQ "0" echo Failed exitCode=%ERRORLEVEL%, command=%_CMD_%
exit /b %ERRORLEVEL%
:error
endlocal
echo An error has occurred during web site deployment.
call :exitSetErrorLevel
call :exitFromFunction 2>nul
:exitSetErrorLevel
exit /b 1
:exitFromFunction
()
:end
endlocal
echo Finished successfully.