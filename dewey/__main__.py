from dewey.gui import App

def main():
    app = App()
    app.after(0, lambda:app.state('zoomed'))
    app.mainloop()

if __name__ == "__main__":
    main()