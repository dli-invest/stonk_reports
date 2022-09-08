# bash script that takes an stonk as an argument and calls fetch_stonk_doc and other scripts to fetch the stonk's data
# Usage: ./fetch_stonks.sh <stonk>

# define conscrap url
conscrap_url="https://github.com/dli-invest/conscrap"
# check if stonk is passed as an argument
if [ -z "$1" ]; then
    echo "No stonk passed as an argument"
    exit 1
fi

# strip .* from $1
stonk=$(echo "$1" | sed 's/\..*//')


# check to make sure REMOTE_SELENIUM_URL is set
if [ -z "$REMOTE_SELENIUM_URL" ]; then
    echo "REMOTE_SELENIUM_URL is not set"
    exit 1
fi
# check to make sure REMOTE_SELENIUM_USERNAME is set
if [ -z "$REMOTE_SELENIUM_USERNAME" ]; then
    echo "REMOTE_SELENIUM_USERNAME is not set"
    exit 1
fi

# check to make sure REMOTE_SELENIUM_PASSWORD is set
if [ -z "$REMOTE_SELENIUM_KEY" ]; then
    echo "REMOTE_SELENIUM_KEY is not set"
    exit 1
fi

# check if dotnet is available on the system
if ! command -v dotnet &> /dev/null
then
    echo "dotnet could not be found"
    exit 1
fi

# check if conscrap is cloned already and if C# is available
if [ ! -d "conscrap" ]; then
    echo "conscrap is not cloned"
    echo "cloning conscrap from $conscrap_url"
    git clone $conscrap_url
fi

# after running python script

# cd to conscrap
cd conscrap
# run conscrap
dotnet run --project ConScrap.Cron $1
# move data/$1 to ../docs/$1
mv data/$1/*.csv ../docs/$stonk/

rm -rf conscrap