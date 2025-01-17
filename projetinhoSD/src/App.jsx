import React, { useEffect, useState } from "react";

const App = () => {
    const [joke, setJoke] = useState("Carregando uma piada...");
    const [secondJoke, setSecondJoke] = useState("Carregando uma segunda piada...");
    const [randomFact, setRandomFact] = useState("Carregando fato aleatório...");
    const [randomFactEs, setRandomFactEs] = useState("Carregando hecho aleatorio...");
    const [currentTime, setCurrentTime] = useState(new Date());

    // Funções para buscar piadas e fatos aleatórios (como antes)
    const fetchJoke = async () => {
        try {
            const jokeResponse = await fetch("https://official-joke-api.appspot.com/random_joke");
            const jokeData = await jokeResponse.json();
            if (jokeData.setup && jokeData.punchline) {
                setJoke(`${jokeData.setup} - ${jokeData.punchline}`);
            } else {
                setJoke("Não foi possível carregar uma piada.");
            }
        } catch (error) {
            console.error("Erro ao carregar piada:", error);
            setJoke("Erro ao carregar piada.");
        }
    };

    const fetchSecondJoke = async () => {
        try {
            const jokeResponseEs = await fetch("https://v2.jokeapi.dev/joke/Any?lang=es&type=single");
            const jokeDataEs = await jokeResponseEs.json();
            if (jokeDataEs.joke) {
                setSecondJoke(jokeDataEs.joke);
            } else if (jokeDataEs.setup && jokeDataEs.delivery) {
                setSecondJoke(`${jokeDataEs.setup} - ${jokeDataEs.delivery}`);
            } else {
                setSecondJoke("No fue posible cargar una broma en español.");
            }
        } catch (error) {
            console.error("Error al cargar broma en español:", error);
            setSecondJoke("Error al cargar broma en español.");
        }
    };

    const fetchRandomFact = async () => {
        try {
            const factResponse = await fetch("https://uselessfacts.jsph.pl/random.json?language=pt");
            const factData = await factResponse.json();
            if (factData.text) {
                setRandomFact(factData.text);
            } else {
                setRandomFact("Não foi possível carregar um fato aleatório.");
            }
        } catch (error) {
            console.error("Erro ao carregar fato aleatório:", error);
            setRandomFact("Erro ao carregar fato aleatório.");
        }
    };

    const fetchRandomFactEs = async () => {
        try {
            const factResponseEs = await fetch("https://uselessfacts.jsph.pl/random.json?language=es");
            const factDataEs = await factResponseEs.json();
            if (factDataEs.text) {
                setRandomFactEs(factDataEs.text);
            } else {
                setRandomFactEs("No se pudo cargar un hecho aleatorio.");
            }
        } catch (error) {
            console.error("Error al cargar hecho aleatorio:", error);
            setRandomFactEs("Error al cargar hecho aleatorio.");
        }
    };

    // Atualizar o tempo a cada segundo
    useEffect(() => {
        fetchJoke();
        fetchSecondJoke();
        fetchRandomFact();
        fetchRandomFactEs();

        const interval = setInterval(() => {
            fetchJoke();
            fetchSecondJoke();
            fetchRandomFact();
            fetchRandomFactEs();

            // Atualizar a hora a cada segundo
            setCurrentTime(new Date());
        }, 10000);

        return () => clearInterval(interval); 
    }, []);

    return (
        <div className="app-container">
            <h1>Your Daily Dose Of Randomness</h1>
            <div className="time-container">
                <p>{currentTime.toLocaleString()}</p>
            </div>
            <div className="content-container">
                <div className="card">
                    <h2>Joke:</h2>
                    <p>{joke}</p>
                </div>
                <div className="card">
                    <h2>Broma:</h2>
                    <p>{secondJoke}</p>
                </div>
                <div className="card">
                    <h2>Random fact:</h2>
                    <p>{randomFact}</p>
                </div>
                <div className="card">
                    <h2>Hecho aleatorio:</h2>
                    <p>{randomFactEs}</p>
                </div>
            </div>
        </div>
    );
};

export default App;
