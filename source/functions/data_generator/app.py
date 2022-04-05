from random import randint

# TODO refactor code to generate data from Vendor A and B
def lambda_handler(event, context):
    """
    # TODO add these scenarios below
    Scenarios:
        Vendor A:
            timeliness
            invalid data
            hourly
        Vendor B:
            timeliness
            daily

    Parameters
    ----------
    event: dict, required
        Input event to the Lambda function

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
        dict: Object containing the current price of the stock
    """
    # Check current price of the stock
    stock_price = randint(
        0, 100
    )  # Current stock price is mocked as a random integer between 0 and 100
    return {"stock_price": stock_price}
