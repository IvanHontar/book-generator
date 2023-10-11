import openai
from math import ceil

# Importing the OpenAI API key from the configuration file
from config import OPENAI_API_KEY

# Setting your OpenAI API key
openai.api_key = OPENAI_API_KEY

# Function to interact with the user and get book information
def get_user_input():
    #topic = input("Enter the topic of the book: ")
    topic = """Contents of the book:
? Introduction on the history and origins of Italian cuisine (maximum 2 pages)
? Talk about Mediterranean cuisine and the differences that characterize it compared to other
types of cuisine.
? Talk about the basic techniques of Italian cuisine
? Talk about the tips and mistakes to avoid for the successful preparation of typical Italian
dishes
? Talk about what pans and equipment are needed to make these types of recipes, and how to
best use them
? Insert conversion tables US - European Measurements (Ounces - Grams, Cups - Millilitres,
Degrees Fahrenheit - Degrees Celsius)
? Enter the 70 recipes. The recipes must be divided into:
20 typical recipes from Northern Italy
20 typical recipes from Central Italy
20 typical recipes from Southern Italy
+ bonus 10 traditional grandmother's recipes.
For each recipe enterthe Region of origin (example: Lazio, Lombardy, Veneto, etc.). Each recipe must
be accompanied by advice on freezing,calorie count, cooking times, list of necessary ingredients
accompanied by the US unit of measurement. (for liquids and solid foods).
Include recipes with more humble ingredients such as:
beans and lentils, inexpensive fishand cuts of meat, garden vegetables, rice, pasta, leftovers.
Insert a collection of Italian pasta recipes perfected over time by people who have spent a lifetime
cooking for love, not for living: Italian grandmothers.
Here is an example of recipes that you can include in the book: Lasagna, Bolognese ragu, Cacio e
Pepe, Favorite Italian biscuits and desserts, Sausage containing fennel seeds, Ricotta cheesecake,
Florentine beef stew, Gnudi with nettle and ricotta and Sicilian watermelon pudding, basil bruschetta,
Romagnola minestrone, Tortelli Stuffed with Parsley and Ricotta, Clam Risotto, Calamari and
Potatoes Genoese style • Chicken alla Hunter, Ossobuco in White, Meatballs and Cherry
Tomatoes, Artichoke Cake, Crispy Fried Courgette Flowers, Insalata di Sunchoke e Spinaci,
Chestnuts boiled in Romagna style red wine, Polenta millefeuille with raisins, dried figs and pine nuts,
Zabaglione, bruschetta with spinach and ricotta, Margherita pizza, etc.
For each section of recipes, North - Center - South, it creates an index with page indications, which
divides the 20 recipes by type of meal in this way: "first courses", "second courses" and "desserts".
? Conclusion (1 Page maximum)"""
    chapters = int(input("Enter the desired number of chapters in the entire book: "))
    words = int(input("Enter the number of words in all book: "))
    style = input("Enter the writing style of the book: ")
    words_per_chapter = ceil(words/chapters)
    return {'topic': topic, 'chapters': chapters, 'style': style, 'words_per_chapter': words_per_chapter}

# Function to generate a book outline using the OpenAI API
def generate_book_plan(user_input):
    prompt = f"Topic of the book: {user_input['topic']}. Number of chapters: {user_input['chapters']}. Writing style: {user_input['style']}. Please provide a general plot and chapter titles for the book. Also you need to numerate all chapters. Write me only names of chapter separated by ; The name of last chapter should be ended by ; "

    # Generating text using the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        n=1,
        stop=None
    )

    # Extracting generated text from the API response
    generated_text = response.choices[0].text.strip().replace("Chapter Titles:", "").replace("Chapter Titles :", "").replace("Chapter titles:", "").replace("Chapter Titles", "").replace("Chapter titles", "").replace("Chapters:", "")
    return generated_text

# Function to save the book outline to a .md file
def save_to_file(book_plan, file_name='book_plan.md'):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(book_plan)

# Function to read the book outline from a .md file
def read_book_plan(file_path='book_plan.md'):
    with open(file_path, 'r', encoding='utf-8') as file:
        book_plan = file.read()
    return book_plan

# Function to generate a full book based on the outline using the OpenAI API
def generate_full_book(book_plan, words_per_chapter):
    prompt = f"Create a full book based on the following plan:\n {book_plan} \n I WANT THIS BOOK TO HAVE {words_per_chapter} WORDS. IT'S VERY IMPORTANT."

    # Generating text using the OpenAI API
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=3500,
            n=1,
            stop=None
        )
    except:
        prompt = [{"role": "user", "context": f"Create a full book based on the following plan:\n {book_plan} \n I WANT THIS BOOK TO HAVE {words_per_chapter} WORDS. IT'S VERY IMPORTANT. Your answer should be like this: 'Your text: '...'. '"}]
        response = openai.ChatCompletion.create(
            engine="gpt-3.5-turbo-16k",
            prompt=prompt,
            n=1,
            stop=None
        )
        while len(response.choices[0].text.strip().replace("Your text: '", "")) < words_per_chapter:
            pass

    # Extracting generated text from the API response
    generated_text = response.choices[0].text.strip().replace("Your text: '", "")
    return generated_text

# Function to save the full book to a .md file
def save_full_book_to_file(full_chapters, file_name='full_book.md', max_words=35000):
    total_words = sum(len(chapter.split()) for chapter in full_chapters)
    if total_words > max_words:
        print(f"Warning: The book exceeds the maximum allowed word count of {max_words} words.")

    with open(file_name, 'w', encoding='utf-8') as file:
        for item in full_chapters:
            file.write(item + '\n\n')

        

def generated_small_chapters(chapters, words_per_chapter, topic):
    small_chapters = []
    for i, chapter in enumerate(chapters):
        if i == 0:
            words_to_generate = words_per_chapter / 2
        elif i == len(chapters) - 1:
            words_to_generate = words_per_chapter / 2
        else:
            words_to_generate = words_per_chapter / 2

        # Генерация текста для главы
        generated_text = ""
        while len(generated_text.split()) < words_to_generate:
            prompt = f"Create a full chapter in English based on name of chapter:\n {chapter} \n I WANT THIS CHAPTER TO HAVE {words_to_generate} WORDS. IT'S VERY IMPORTANT. The topic of this book: \n {topic} \n . Your answer should be like this: 'Chapter number ... : \n\n ...'."
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                n=1,
                stop=None
            )
            generated_text = response.choices[0].text.strip()
        
        small_chapters.append(generated_text)

    return small_chapters


def generate_full_chapters(small_chapters, words_per_chapter):
    full_chapters = []
    for small_chapter in small_chapters:
        generated_text = small_chapter
        while len(generated_text.split()) < words_per_chapter:
            prompt = f"Extend the chapter:\n\n{generated_text}\n\nAdd more details or actions to the chapter so that it is longer than {words_per_chapter} words. Your answer should be like this: 'Chapter number ... : \n\n ...'."
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                n=1,
                stop=None
            )
            additional_text = response.choices[0].text.strip()
            generated_text += "\n\n" + additional_text
        
        full_chapters.append(generated_text)

    return full_chapters

    


# Main function of the program
def main():
    # Getting user input and generating a book outline
    user_input = get_user_input()
    book_plan = generate_book_plan(user_input)
    words_per_chapter = user_input['words_per_chapter']
    
    
    # Saving the book outline to a file
    save_to_file(book_plan)
    chapters = book_plan.split("\n")
    try:
        chapters.remove(" ")
    except:
        pass
    try:
        chapters.remove("")
    except:
        pass
    print(chapters)
    small_chapters = generated_small_chapters(chapters, words_per_chapter, user_input['topic'])
    print(small_chapters)
    print(len(small_chapters))
    save_full_book_to_file(small_chapters)
    full_chapters = generate_full_chapters(small_chapters, words_per_chapter, chapters)

    # Saving the full book to a file
    save_full_book_to_file(full_chapters)

    print("Book plan saved in the 'book_plan.md' file.")
    print("Full book saved in the 'full_book.md' file.")

# Running the program
if __name__ == "__main__":
    main()
