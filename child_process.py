my_file = open('file.txt', 'w')
cond = True


if __name__ == '__main__':
    # Infinite loop
    while cond:
        try:
            my_value = input(':')  # get console input (STDIN)

            if my_value == 'kill':
                # if main process sends 'kill', the loop breaks and stop this process
                cond = False
            else:
                # write data to file
                my_file.write(str(my_value) + '\n')
        except EOFError:
            # line parsing error
            pass

    my_file.close()  # close file on loop exits
