import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [temperaturaAtual, setTemperaturaAtual] = useState(33.8);
  const [sensacaoTermica, setSensacaoTermica] = useState(30.2);
  const [eventos, setEventos] = useState([
    { data: "03/04/2024", hora: "14:20", temperatura: "46,8ºC" },
    { data: "02/04/2024", hora: "09:15", temperatura: "45,5ºC" },
    { data: "29/03/2024", hora: "02:05", temperatura: "46,1ºC" },
    { data: "28/03/2024", hora: "11:45", temperatura: "45,7ºC" },
  ]);

  const [dataHoraAtual, setDataHoraAtual] = useState("");

  useEffect(() => {
    const now = new Date();
    const data = now.toLocaleDateString("pt-BR");
    const hora = now.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
    setDataHoraAtual(`${data} ${hora}`);
  }, []);

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
          <p className="temperatura">{temperaturaAtual.toFixed(1)}ºC</p>
          <p className="sensacao">Sensação térmica: {sensacaoTermica.toFixed(1)}ºC</p>
        </div>
      </div>

      <div className="eventos">
        <div className="header">
          <h2>Eventos de Temperatura</h2>
          <label>
            Filtro:
            <select>
              <option>Últimos 30 dias</option>
              <option>Últimos 15 dias</option>
              <option>Últimos 7 dias</option>
            </select>
          </label>
        </div>

        <table>
          <thead>
            <tr>
              <th>Data</th>
              <th>Hora</th>
              <th>Temperatura</th>
            </tr>
          </thead>
          <tbody>
            {eventos.map((evento, index) => (
              <tr key={index}>
                <td>{evento.data}</td>
                <td>{evento.hora}</td>
                <td>{evento.temperatura}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;