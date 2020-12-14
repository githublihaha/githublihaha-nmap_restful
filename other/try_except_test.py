def test():
    try:
        print('first try')
        return 'first try'
    except:
        return 'first except'
    finally:
        # start scan
        try:
            print('second try')
        except :
            result = 123
            code = 400
        else:
            code = 200
        finally:
            print('finally')


test()


