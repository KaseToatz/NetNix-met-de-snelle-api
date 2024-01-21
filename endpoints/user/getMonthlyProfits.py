from fastapi.responses import JSONResponse

from src import Endpoint, Method, Connection, UserType

class GetMonthlyProfits(Endpoint):

    async def callback(self) -> JSONResponse:

        async with Connection(UserType.JUNIOR) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT Subscription, referd_by_acount FROM Acount")
                acounts = await cursor.fetchall()
                if not acounts:
                    return JSONResponse({"error": "There aren't any acounts yet."}, 400)
                profits = 0
                for acount in acounts: 
                    subscription = acount[0]
                    referd_by_acount = acount[1]
                    if subscription != 0:
                        if subscription == 1:
                            profits += 7.99
                        elif subscription == 2:
                            profits += 10.99
                        elif subscription == 3:
                            profits +=13.99
                        if referd_by_acount != 0:
                            profits -= 2       

                return JSONResponse({profits})
            
def setup() -> GetMonthlyProfits:
    return GetMonthlyProfits(Method.GET, "/user/getMonthlyProfits", JSONResponse)