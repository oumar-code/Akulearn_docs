@echo off
setlocal
set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%
set DEFAULT_JVM_OPTS=
set GRADLE_EXIT_CONSOLE=false

set CMD_LINE_ARGS=
:parseArgs
if "%1"=="" goto execute
set CMD_LINE_ARGS=%CMD_LINE_ARGS% "%1"
shift
goto parseArgs
:execute
set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar
java %DEFAULT_JVM_OPTS% -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %CMD_LINE_ARGS%
endlocal
