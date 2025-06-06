import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [temperaturaAtual, setTemperaturaAtual] = useState(null);
  const [sensacaoTermica, setSensacaoTermica] = useState(null);
  const [filtroDias, setFiltroDias] = useState(30);
  const [animarTemp, setAnimarTemp] = useState(false);
  const [paginaAtual, setPaginaAtual] = useState(1);
  const [totalPaginas, setTotalPaginas] = useState(1);

  const [animarSensacao, setAnimarSensacao] = useState(false);

  const [eventos, setEventos] = useState([]);

  const [dataHoraAtual, setDataHoraAtual] = useState("");

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      const data = now.toLocaleDateString("pt-BR");
      const hora = now.toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
      });
      setDataHoraAtual(`${data} ${hora}`);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws/climate-records");

    let temperatura = null;
    let umidade = null;

    socket.onopen = () => {
      console.log("WebSocket conectado");
    };

    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        console.log("Recebido:", payload);

        payload.forEach((entry) => {
          const name = entry.variable_name?.toLowerCase();
          const value = parseFloat(entry.last_value);

          if (name === "temperature") {
            temperatura = value;
          }

          if (name === "humidity") {
            umidade = value;
          }
        });

        if (temperatura !== null) {
          setTemperaturaAtual(temperatura);
          setAnimarTemp(true);
          setTimeout(() => setAnimarTemp(false), 500);
        }

        if (temperatura !== null && umidade !== null) {
          const hi =
            temperatura - 0.55 * (1 - umidade / 100) * (temperatura - 14.5);
          setSensacaoTermica(hi);
          setAnimarSensacao(true);
          setTimeout(() => setAnimarSensacao(false), 500);
        }
      } catch (err) {
        console.error("Erro ao processar mensagem:", err);
      }
    };

    socket.onerror = (error) => {
      console.error("Erro no WebSocket:", error);
    };

    socket.onclose = () => {
      console.log("Conexão WebSocket encerrada");
    };

    return () => {
      socket.close();
    };
  }, []);

  useEffect(() => {
    fetch(
      `http://localhost:8000/climate-records?page=${paginaAtual}&quantity_records=5`,
      {
        headers: {
          Accept: "application/json",
        },
      }
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erro ao buscar eventos");
        }
        return response.json();
      })
      .then((data) => {
        const eventosFormatados = data.records.map((item) => {
          const dataHora = new Date(item.created_at);
          return {
            data: dataHora.toLocaleDateString("pt-BR"),
            hora: dataHora.toLocaleTimeString("pt-BR", {
              hour: "2-digit",
              minute: "2-digit",
            }),
            temperatura: `${item.temperature.toFixed(1)}ºC`,
            sensacao: `${item.thermal_sensation.toFixed(1)}ºC`,
          };
        });

        setEventos(eventosFormatados);
        setTotalPaginas(data.total_pages);
      })
      .catch((error) => {
        console.error("Erro ao buscar eventos:", error);
      });
  }, [paginaAtual]);

  const eventosFiltrados = eventos.filter((evento) => {
    const [dia, mes, ano] = evento.data.split("/");
    const dataEvento = new Date(`${ano}-${mes}-${dia}`);
    const dataLimite = new Date();
    dataLimite.setDate(dataLimite.getDate() - filtroDias);
    return dataEvento >= dataLimite;
  });

  const corPreenchimento = temperaturaAtual <= 22 ? "blue" : "red";

  return (
    <div className="container">
      <h1>Temperatura Ambiente</h1>
      <p className="data-hora">{dataHoraAtual}</p>

      <div className="termometro-box">
        <div className="custom-thermometer">
          <div
            className="custom-thermometer-fill"
            style={{
              height: `${(temperaturaAtual / 60) * 100}%`,
              backgroundColor: corPreenchimento,
            }}
          ></div>
        </div>
        <div className="temperatura-info">
          {temperaturaAtual === null || sensacaoTermica === null ? (
            <div className="loading-temp">
              <div className="spinner-wrapper">
                <div className="spinner"></div>
                <p>Carregando temperatura...</p>
              </div>
            </div>
          ) : (
            <>
              <p className={`temperatura ${animarTemp ? "animar" : ""}`}>
                {temperaturaAtual.toFixed(1)}ºC
              </p>
              <p className={`sensacao ${animarSensacao ? "animar" : ""}`}>
                Sensação térmica: {sensacaoTermica.toFixed(1)}ºC
              </p>
            </>
          )}
        </div>
      </div>

      <div className="eventos">
        <div className="header">
          <h2>Eventos de Temperatura</h2>
          <label>
            Filtro:
            <select
              value={filtroDias}
              onChange={(e) => setFiltroDias(Number(e.target.value))}
            >
              <option value={30}>Últimos 30 dias</option>
              <option value={15}>Últimos 15 dias</option>
              <option value={7}>Últimos 7 dias</option>
            </select>
          </label>
        </div>
        <div className="tabela-wrapper">
          <table>
            <thead>
              <tr>
                <th>Data</th>
                <th>Hora</th>
                <th>Temperatura</th>
                <th>Sensação Térmica</th>
              </tr>
            </thead>

            <tbody>
              {eventosFiltrados.map((evento, index) => (
                <tr key={index}>
                  <td>{evento.data}</td>
                  <td>{evento.hora}</td>
                  <td>{evento.temperatura}</td>
                  <td>{evento.sensacao}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="aviso-scroll">🔁 Role a tabela para o lado →</p>
      </div>
      <div className="paginacao-numerica">
        <span>Página:</span>

        {paginaAtual > 3 && totalPaginas > 5 && (
          <button
            onClick={() => setPaginaAtual((prev) => Math.max(prev - 5, 1))}
          >
            «
          </button>
        )}

        {(() => {
          const paginas = [];

          let start = Math.max(1, paginaAtual - 2);
          let end = Math.min(totalPaginas, start + 4);

          if (end - start < 4) {
            start = Math.max(1, end - 4);
          }

          for (let i = start; i <= end; i++) {
            paginas.push(
              <button
                key={i}
                onClick={() => setPaginaAtual(i)}
                className={i === paginaAtual ? "ativo" : ""}
              >
                {i}
              </button>
            );
          }

          return paginas;
        })()}

        {paginaAtual < totalPaginas - 2 && totalPaginas > 5 && (
          <button
            onClick={() =>
              setPaginaAtual((prev) => Math.min(prev + 5, totalPaginas))
            }
          >
            »
          </button>
        )}
      </div>
    </div>
  );
}

export default App;
