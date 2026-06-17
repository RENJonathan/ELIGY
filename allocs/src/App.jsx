import { useState } from "react";
import "./App.css";
 
const NATIONALITIES = [
  "Algérienne","Allemande","Américaine","Anglaise","Belge","Brésilienne",
  "Camerounaise","Canadienne","Chinoise","Congolaise","Espagnole","Française",
  "Ivoirienne","Italienne","Japonaise","Marocaine","Mexicaine","Néerlandaise",
  "Portugaise","Roumaine","Russe","Sénégalaise","Suisse","Tunisienne","Turque",
  "Autre"
];
 
const COUNTRIES = [
  "Allemagne","Belgique","Brésil","Canada","Côte d'Ivoire","Espagne",
  "États-Unis","France","Italie","Japon","Maroc","Mexique","Pays-Bas",
  "Portugal","Roumanie","Russie","Sénégal","Suisse","Tunisie","Turquie",
  "Autre"
];
 
export default function Allocs() {
  const [form, setForm] = useState({ age: "", nationalite: "", pays: "" });
  const [submitted, setSubmitted] = useState(false);
  const [errors, setErrors] = useState({});
 
  const validate = () => {
    const e = {};
    if (!form.age || isNaN(form.age) || form.age < 1 || form.age > 120)
      e.age = "Veuillez entrer un âge valide (1–120).";
    if (!form.nationalite) e.nationalite = "Veuillez sélectionner votre nationalité.";
    if (!form.pays) e.pays = "Veuillez sélectionner votre pays de résidence.";
    return e;
  };
 
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: undefined });
  };
 
  const handleSubmit = () => {
    const e = validate();
    if (Object.keys(e).length) { setErrors(e); return; }
    setSubmitted(true);
  };
 
  const handleReset = () => {
    setForm({ age: "", nationalite: "", pays: "" });
    setErrors({});
    setSubmitted(false);
  };
 
  return (
    <>
      <div className="page">
        {/* HEADER */}
        <header className="header">
          <div className="header-inner">
            <div className="logo-badge">
              <div className="logo-dot">A</div>
              <span className="logo-label">Allocs</span>
            </div>
            <h1 className="headline">
              Vos droits aux <span>allocations</span>,<br />en un instant.
            </h1>
            <p className="subhead">
              Renseignez votre profil pour découvrir les aides auxquelles vous êtes éligible selon votre situation.
            </p>
          </div>
        </header>
 
        <svg className="wave" viewBox="0 0 1440 54" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" style={{display:'block',marginTop:'-1px',background:'#FAFAF8'}}>
          <path d="M0,0 C360,54 1080,54 1440,0 L1440,54 L0,54 Z"
            fill="url(#waveGrad)" />
          <defs>
            <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#F5A623"/>
              <stop offset="50%" stopColor="#F7C948"/>
              <stop offset="100%" stopColor="#2ECC71"/>
            </linearGradient>
          </defs>
        </svg>
 
        {/* MAIN */}
        <main className="main">
          <div className="card">
            {!submitted ? (
              <>
                <h2 className="card-title">Votre profil</h2>
                <p className="card-subtitle">Tous les champs sont requis pour continuer.</p>
 
                {/* AGE */}
                <div className="field">
                  <label className="field-label">
                    <span className="field-icon icon-age">🎂</span>
                    Âge
                  </label>
                  <input
                    type="number"
                    name="age"
                    min="1" max="120"
                    placeholder="Ex : 28"
                    value={form.age}
                    onChange={handleChange}
                    className={errors.age ? "err" : ""}
                  />
                  {errors.age && <p className="field-error">{errors.age}</p>}
                </div>
 
                {/* NATIONALITÉ */}
                <div className="field">
                  <label className="field-label">
                    <span className="field-icon icon-nat">🌍</span>
                    Nationalité
                  </label>
                  <div className="select-wrap">
                    <select
                      name="nationalite"
                      value={form.nationalite}
                      onChange={handleChange}
                      className={errors.nationalite ? "err" : ""}
                    >
                      <option value="">Sélectionner…</option>
                      {NATIONALITIES.map(n => <option key={n} value={n}>{n}</option>)}
                    </select>
                  </div>
                  {errors.nationalite && <p className="field-error">{errors.nationalite}</p>}
                </div>
 
                {/* PAYS DE RÉSIDENCE */}
                <div className="field">
                  <label className="field-label">
                    <span className="field-icon icon-pays">🏡</span>
                    Pays de résidence
                  </label>
                  <div className="select-wrap">
                    <select
                      name="pays"
                      value={form.pays}
                      onChange={handleChange}
                      className={errors.pays ? "err" : ""}
                    >
                      <option value="">Sélectionner…</option>
                      {COUNTRIES.map(c => <option key={c} value={c}>{c}</option>)}
                    </select>
                  </div>
                  {errors.pays && <p className="field-error">{errors.pays}</p>}
                </div>
 
                <button className="btn-submit" onClick={handleSubmit}>
                  Vérifier mes droits →
                </button>
              </>
            ) : (
              <div className="success">
                <div className="success-icon">✓</div>
                <h2 className="success-title">Profil enregistré !</h2>
                <p className="success-text">
                  Nous analysons votre éligibilité aux allocations sur la base de votre profil.
                </p>
                <div className="summary">
                  <div className="summary-row">
                    <span className="summary-key">Âge</span>
                    <span className="summary-val">{form.age} ans</span>
                  </div>
                  <div className="summary-row">
                    <span className="summary-key">Nationalité</span>
                    <span className="summary-val">{form.nationalite}</span>
                  </div>
                  <div className="summary-row">
                    <span className="summary-key">Pays de résidence</span>
                    <span className="summary-val">{form.pays}</span>
                  </div>
                </div>
                <button className="btn-reset" onClick={handleReset}>
                  Modifier mon profil
                </button>
              </div>
            )}
          </div>
        </main>
 
        {/* FOOTER */}
        <footer className="footer">
          © 2026 <span>Allocs</span> — Tous droits réservés
        </footer>
      </div>
    </>
  );
}