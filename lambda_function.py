import main  # Import your main.py module

def lambda_handler(event, context):
    # Call your main function from main.py
    main.main_function()

    # You can also pass event and context parameters to your main function if needed
    # main.main_function(event, context)

    # Optional: Return a response
    return {
        'statusCode': 200,
        'body': 'Lambda function executed successfully'
    }