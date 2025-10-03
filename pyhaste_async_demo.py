import asyncio
import time
from random import uniform

from pyhaste.async_analyzer import measure, measure_wrap, report


@measure_wrap("prepare")
async def prepare():
    await asyncio.sleep(uniform(0.05, 0.15))


async def find_items():
    print("Finding items")
    await asyncio.sleep(uniform(0.05, 0.15))
    return [1, 2, 3]


async def process_item_more(item: int):
    with measure("do_stuff.process_item.process_item_more"):
        await asyncio.sleep(uniform(0.05, 0.15))
        print(f"Processed {item} further")
        return item * 1.5


async def process_item(item: int):
    with measure("do_stuff.process_item"):
        print(f"Processing {item}")
        data = await process_item_more(item)
        await asyncio.sleep(uniform(0.05, 0.15))
        return data**2


async def save_item():
    with measure("do_stuff.save_item"):
        print("Saving items")
        await asyncio.sleep(uniform(0.01, 0.02))


@measure_wrap("do_stuff")
async def do_stuff():
    with measure("do_stuff.find_items"):
        items = await find_items()
    awaits = []
    for item in items:
        awaits.append(process_item(item))
    await asyncio.gather(*awaits)
    await save_item()


async def main():
    await prepare()

    await asyncio.sleep(uniform(0.1, 0.25))

    elapsed = 0
    while elapsed < 1.5:
        start = time.perf_counter()

        with measure("do_stuff"):
            await do_stuff()

        elapsed += time.perf_counter() - start

    await asyncio.sleep(uniform(0.1, 0.25))

    report()


if __name__ == "__main__":
    asyncio.run(main())
