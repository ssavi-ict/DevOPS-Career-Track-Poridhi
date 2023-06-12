import { useState, useEffect } from "react";
import { Form } from "./Form";
import { News } from "./News";
import { getNews, createNews } from "../lib/db";

const App = () => {
  const [newsList, setNewsList] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [isCache, setIsCache] = useState(false);

  // set news on first render
  useEffect(() => {
    getNews()
      .then(({isCached, news}) => {
        setNewsList(news);
        setIsCache(isCached);
      })
      .catch((error) => console.error(error));
  }, []);

  // handle form submit
  const handleSubmit = async () => {
    try {
      await createNews(userInput);
      const {isCached, news} = await getNews();
      setNewsList(news);
      setIsCache(isCached);
    } catch (error) {
      console.error("Error creating news: ", error);
    }
  };

  const handleRefresh = async () => {
    const {isCached, news} = await getNews();
    setNewsList(news);
    setIsCache(isCached);
  };

  return (
    <main className="grid place-items-center my-10 grid-cols-1 md:grid-cols-2">
      <section>
        <Form setUserInput={setUserInput} handleSubmit={handleSubmit} />
      </section>
      <section>
        <button
            className="block mx-auto mb-5 px-2 py-1 bg-gray-500 text-white rounded-md"
            onClick={handleRefresh}
          >
            ↻ Refresh
          </button>
          <News newsList={newsList} isCache={isCache} />
      </section>
    </main>
  );
};

export default App;

/*import { useState, useEffect } from "react";
import { Form } from "./Form";
import { News } from "./News";
import { getNews, createNews } from "../lib/db";

const App = () => {
  const [newsList, setNewsList] = useState([]);
  const [userInput, setUserInput] = useState("");

  // set news on first render
  useEffect(() => {
    getNews()
    .then((news) => {console.log(news)
    return news})
      .then((news) => setNewsList(news))
      .catch((error) => console.error(error));
  }, []);

  // handle form submit
  const handleSubmit = async () => {
    try {
      await createNews(userInput);
      const latesetNewsList = await getNews();
      setNewsList(latesetNewsList);
    } catch (error) {
      console.error("Error creating news: ", error);
    }
  };

  return (
    <main className="grid place-items-center my-10 grid-cols-1 md:grid-cols-2">
      <section>
        <Form setUserInput={setUserInput} handleSubmit={handleSubmit} />
      </section>
      <section>
        <h3 className="text-2xl font-bold text-center">
          News List{" "}
          <span className="text-sm text-gray-500">({newsList.length})</span>
        </h3>
        {newsList && Array.isArray(newsList) && newsList.map((news) => (
          <News key={news.id} text={news.text} />
        ))}
      </section>
    </main>
  );
};

export default App;*/