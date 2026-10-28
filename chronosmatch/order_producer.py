"""Generate mock orders into the single-process mmap prototype."""
import asyncio
import random
import time
from shared_bus import SharedBus


async def produce(bus, total_orders=100_000):
    price = 100_000
    published = 0
    for order_id in range(1, total_orders + 1):
        price += random.randint(-2, 2)
        side = random.choice((1, -1))
        qty = random.randint(1, 100)
        while not bus.publish(order_id, side, price, qty, time.perf_counter_ns()):
            await asyncio.sleep(0)
        published += 1
        if order_id % 1000 == 0:
            await asyncio.sleep(0)
    print(f"Published {published:,} orders")


async def main():
    bus = SharedBus()
    try:
        await produce(bus)
    finally:
        bus.close()


if __name__ == "__main__":
    asyncio.run(main())
