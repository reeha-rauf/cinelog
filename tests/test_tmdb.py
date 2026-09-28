import asyncio
from app.movies.tmdb import search_movies

async def main():
    result = await search_movies("Inception")
    print(result)

asyncio.run(main())