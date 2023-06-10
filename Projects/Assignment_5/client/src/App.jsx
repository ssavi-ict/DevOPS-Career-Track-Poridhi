import { useState } from "react";
import { Form } from "./Form";
import { News } from "./News";

const newsData = [
  { id: 1, text: "Hello There ..."},
  { id: 2, text: "How Are You ..."},
  { id: 3, text: "What is your name ... "},
  { id: 4, text: "Where are you from ... "},
  { id: 5, text: "Are you OK ... "},
];

const App = () =>{
  const [newsList, setNewsList] = useState(newsData);
  const [userInput, setUserInput] = useState("");

  const handleSubmit = () => {
    const latestNewsList = [
      ...newsList,
      {id: newsList.length + 1, text: userInput},
    ];
    
    setNewsList(latestNewsList);
    setUserInput("");
  };

  return(
    <main className="grid place-items-center my-10 grid-cols-1 md:grid-cols-2">
      <section>
        <Form setUserInput={setUserInput} handleSubmit={handleSubmit} />
      </section>
      <section>
        <h3 className="text-2x1 font-bold text-center">
          News List {" "}
          <span className="text-sm text-gray-500">({newsList.length})</span>
        </h3>
        {
          newsList.map((news) => (
            <News key={news.id} text={news.text} />
          )
          )
        }
      </section>
    </main>
  )

};

export default App;