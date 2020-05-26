# gone_with_the_wind

an async server that fetches weather and movies

## installation instructions
install [pipenv](https://github.com/pypa/pipenv) and run:

    pipenv install
    ./run

## design considerations:
- prefer libraries over inventing the wheel
- as safe as possible url fetching 
- use asyncio to prevent blocking while a 