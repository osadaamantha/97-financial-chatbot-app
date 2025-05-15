import React from "react";
import "./SummaryCard.css";

const SummaryCard = ({ title, value }) => {
  return (
    <div className="summary-card">
      <h3>{title}</h3>
      <p>{value.toLocaleString()}</p>
    </div>
  );
};

export default SummaryCard;
