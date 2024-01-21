from fastapi.responses import JSONResponse

from src import Endpoint, Method, Connection, UserType

class GetMonthlyProfits(Endpoint):

    async def callback(self) -> JSONResponse:

        async with Connection(UserType.JUNIOR) as db:
            async with db.cursor() as cursor:
                await cursor.callproc("get_subscription_data") 
                results = await cursor.fetchall()
                if not results:
                    return JSONResponse({"error": "There aren't any subscriptions yet."}, 400)
                profits = 0
                for result in results:
                    profits += result[3]

                return JSONResponse({profits})
            
def setup() -> GetMonthlyProfits:
    return GetMonthlyProfits(Method.GET, "/user/getMonthlyProfits", JSONResponse)