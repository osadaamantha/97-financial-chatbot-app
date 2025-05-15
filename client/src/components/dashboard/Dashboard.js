import React, { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, Legend
} from "recharts";
import "../../App.css";

function Dashboard() {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState("DIPPED PRODUCTS PLC");
  const [selectedYear, setSelectedYear] = useState("All Years");
  const [selectedYearRange, setSelectedYearRange] = useState("All Years");
  const [selectedQuarterRange, setSelectedQuarterRange] = useState("Q1-Q4");

  const yearRanges = [
    { label: "All Years", value: "All Years" },
    { label: "2022 to 2023", value: "2022-2023" },
    { label: "2023 to 2024", value: "2023-2024" },
    { label: "2022 to 2024", value: "2022-2024" },
  ];

  const quarterRanges = [
    { label: "Q1 to Q2", value: "Q1-Q2" },
    { label: "Q1 to Q3", value: "Q1-Q3" },
    { label: "Q2 to Q3", value: "Q2-Q3" },
    { label: "Q2 to Q4", value: "Q2-Q4" },
    { label: "Q3 to Q4", value: "Q3-Q4" },
    { label: "All Quarters", value: "Q1-Q4" },
  ];

  const quarterOrder = ["Q1", "Q2", "Q3", "Q4"];

  useEffect(() => {
    fetch("http://localhost:8080/api/financial-data")
      .then((res) => res.json())
      .then((rawData) => {
        const formattedData = rawData.map((row) => {
          const period = row.PeriodStartEnd;
          const startDate = period?.split(" - ")[0]?.trim();
          const year = startDate?.slice(0, 4);
          const startMonth = parseInt(startDate?.split("-")[1]);
          let quarter = "Unknown";
          if (startMonth >= 1 && startMonth <= 3) quarter = "Q1";
          else if (startMonth >= 4 && startMonth <= 6) quarter = "Q2";
          else if (startMonth >= 7 && startMonth <= 9) quarter = "Q3";
          else if (startMonth >= 10 && startMonth <= 12) quarter = "Q4";

          return {
            ...row,
            Revenue: parseFloat(row.Revenue || 0),
            COGS: parseFloat(row.COGS || 0),
            GrossProfit: parseFloat(row.GrossProfit || 0),
            OtherOperatingIncome: parseFloat(row.OtherOperatingIncome || 0),
            DistributionCosts: parseFloat(row.DistributionCosts || 0),
            OtherOperatingExpense: parseFloat(row.OtherOperatingExpense || 0),
            NetIncome: parseFloat(row.NetIncome || 0),
            Year: year || "Unknown",
            Quarter: quarter,
          };
        });
        setData(formattedData);
      });
  }, []);

  useEffect(() => {
    const [startQ, endQ] = selectedQuarterRange.split("-");
    const startQIndex = quarterOrder.indexOf(startQ);
    const endQIndex = quarterOrder.indexOf(endQ);
    const [startY, endY] = selectedYearRange.split("-");

    const filtered = data.filter((row) => {
      const qIndex = quarterOrder.indexOf(row.Quarter);
      const inQuarterRange = qIndex >= startQIndex && qIndex <= endQIndex;
      const inYearRange =
        selectedYearRange === "All Years" ||
        (row.Year >= startY && row.Year <= endY);
      const inSoloYear =
        selectedYear === "All Years" || row.Year === selectedYear;

      return (
        row.CompanyName === selectedCompany &&
        inQuarterRange &&
        inYearRange &&
        inSoloYear
      );
    });

    setFilteredData(filtered);
  }, [data, selectedCompany, selectedYear, selectedYearRange, selectedQuarterRange]);

  const total = (key) => filteredData.reduce((sum, row) => sum + row[key], 0);

  return (
    <div className="dashboard">
      <div className="filters">
        <div>
          <label>COMPANY</label>
          <select onChange={(e) => setSelectedCompany(e.target.value)} value={selectedCompany}>
            <option>DIPPED PRODUCTS PLC</option>
            <option>Richard Pieris Exports PLC</option>
          </select>
        </div>

        <div>
          <label>YEAR</label>
          <select onChange={(e) => setSelectedYear(e.target.value)} value={selectedYear}>
            <option>All Years</option>
            {[...new Set(data.map((row) => row.Year))].filter(Boolean).sort().map((year) => (
              <option key={year}>{year}</option>
            ))}
          </select>
        </div>

        <div>
          <label>YEAR RANGE</label>
          <select onChange={(e) => setSelectedYearRange(e.target.value)} value={selectedYearRange}>
            {yearRanges.map((yr) => (
              <option key={yr.value} value={yr.value}>{yr.label}</option>
            ))}
          </select>
        </div>

        <div>
          <label>QUARTER RANGE</label>
          <select onChange={(e) => setSelectedQuarterRange(e.target.value)} value={selectedQuarterRange}>
            {quarterRanges.map((qr) => (
              <option key={qr.value} value={qr.value}>{qr.label}</option>
            ))}
          </select>
        </div>
      </div>

      <button className="clear-button" onClick={() => {
        setSelectedCompany("DIPPED PRODUCTS PLC");
        setSelectedYear("All Years");
        setSelectedYearRange("All Years");
        setSelectedQuarterRange("Q1-Q4");
      }}>Clear Filters</button>

      <div className="kpi-cards">
        <div className="kpi-card"><h3>Revenue</h3><p>{total("Revenue").toLocaleString()}</p></div>
        <div className="kpi-card"><h3>COGS</h3><p>{total("COGS").toLocaleString()}</p></div>
        <div className="kpi-card"><h3>Gross Profit</h3><p>{total("GrossProfit").toLocaleString()}</p></div>
        <div className="kpi-card"><h3>Net Income</h3><p>{total("NetIncome").toLocaleString()}</p></div>
      </div>

      <div className="chart-section">
        <h3>Revenue vs COGS</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={filteredData}>
            <XAxis dataKey="PeriodStartEnd" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="Revenue" fill="#3498db" />
            <Bar dataKey="COGS" fill="#e67e22" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-section">
        <h3>Net Income</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={filteredData}>
            <XAxis dataKey="PeriodStartEnd" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="NetIncome" fill="#2ecc71" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-section">
        <h3>Gross Profit Margin (%)</h3>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={filteredData.map((d) => ({
            ...d,
            margin: d.Revenue ? ((d.GrossProfit / d.Revenue) * 100).toFixed(2) : 0,
          }))}>
            <XAxis dataKey="PeriodStartEnd" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="margin" stroke="#8e44ad" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default Dashboard;
