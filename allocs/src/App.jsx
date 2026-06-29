import { useState } from "react";
import "./App.css";

const INITIAL_FORM = {
  age: "",
  countryOfResidence: "FR",
  nationalityZone: "FR",
  monthsInFrancePerYear: "12",
  monthsOfStableResidence: "",
  isDetachedWorker: false,
  hasStableResidenceRight: true,
  hasWorkPermittingVisa: true,
  yearsOfRegularResidence: "",
  hasResidentCard: false,
  isRefugeeOrProtected: false,
  isStateless: false,
  isIsolatedParentWithChildUnder3: false,
  monthlyNetSocialIncome: "",
  householdTotalResources: "",
  dependentChildrenCount: "0",
  childrenMaxAge: "0",
  currentStatus: "employee",
};

const STATUS_OPTIONS = [
  ["employee", "Salarié(e)"],
  ["self_employed", "Indépendant(e)"],
  ["partial_unemployment", "Chômage partiel"],
  ["technical_unemployment", "Chômage technique"],
  ["student", "Étudiant(e), apprenti(e) ou stagiaire"],
  ["other", "Autre situation"],
];

const BENEFIT_ACTION_URLS = {
  "Prime d'activité": "https://www.caf.fr/allocataires/aides-et-demarches/droits-et-prestations/vie-professionnelle/la-prime-d-activite",
  "Aide Médicale de l'État (AME)": "https://www.service-public.gouv.fr/particuliers/vosdroits/F3079",
  "Allocations Familiales": "https://www.caf.fr/allocataires/aides-et-demarches/droits-et-prestations/vie-personnelle/les-allocations-familiales-af",
};

function NumberField({ name, label, value, onChange, min = 0, max, suffix, error }) {
  return (
    <div className="field">
      <label htmlFor={name}>{label}</label>
      <div className="input-with-suffix">
        <input
          id={name}
          name={name}
          type="number"
          min={min}
          max={max}
          value={value}
          onChange={onChange}
          className={error ? "err" : ""}
          required
        />
        {suffix && <span>{suffix}</span>}
      </div>
      {error && <p className="field-error">{error}</p>}
    </div>
  );
}

function YesNoField({ name, label, value, onChange }) {
  return (
    <fieldset className="field yes-no">
      <legend>{label}</legend>
      <div className="segmented">
        <label className={value ? "selected" : ""}>
          <input type="radio" name={name} checked={value} onChange={() => onChange(name, true)} />
          Oui
        </label>
        <label className={!value ? "selected" : ""}>
          <input type="radio" name={name} checked={!value} onChange={() => onChange(name, false)} />
          Non
        </label>
      </div>
    </fieldset>
  );
}

function buildPayload(form) {
  return {
    identity: {
      age: Number(form.age),
      country_of_residence: form.countryOfResidence,
      nationality_zone: form.nationalityZone,
      months_in_france_per_year: Number(form.monthsInFrancePerYear),
      months_of_stable_residence: Number(form.monthsOfStableResidence),
      is_detached_worker: form.isDetachedWorker,
      has_stable_residence_right: form.hasStableResidenceRight,
      has_work_permitting_visa: form.hasWorkPermittingVisa,
      years_of_regular_residence: Number(form.yearsOfRegularResidence || 0),
      has_resident_card: form.hasResidentCard,
      is_refugee_or_protected: form.isRefugeeOrProtected,
      is_stateless: form.isStateless,
      is_isolated_parent_with_child_under_3: form.isIsolatedParentWithChildUnder3,
    },
    income: {
      monthly_net_social_income: Number(form.monthlyNetSocialIncome),
      household_total_resources: Number(form.householdTotalResources),
    },
    family: {
      dependent_children_count: Number(form.dependentChildrenCount),
      children_max_age: Number(form.childrenMaxAge || 0),
    },
    current_status: form.currentStatus,
  };
}

function validate(form) {
  const errors = {};
  const requiredNumbers = [
    ["age", "Indiquez votre âge."],
    ["monthsInFrancePerYear", "Indiquez le nombre de mois."],
    ["monthsOfStableResidence", "Indiquez la durée de résidence."],
    ["monthlyNetSocialIncome", "Indiquez votre revenu mensuel (0 si aucun)."],
    ["householdTotalResources", "Indiquez les ressources du foyer (0 si aucune)."],
    ["dependentChildrenCount", "Indiquez le nombre d’enfants."],
  ];
  requiredNumbers.forEach(([name, message]) => {
    if (form[name] === "" || Number(form[name]) < 0) errors[name] = message;
  });
  if (Number(form.age) > 120) errors.age = "L’âge doit être compris entre 0 et 120 ans.";
  if (Number(form.monthsInFrancePerYear) > 12) errors.monthsInFrancePerYear = "Maximum : 12 mois.";
  if (Number(form.dependentChildrenCount) > 0 && form.childrenMaxAge === "") {
    errors.childrenMaxAge = "Indiquez l’âge de l’enfant le plus âgé.";
  }
  if (form.nationalityZone === "OTHER" && form.yearsOfRegularResidence === "") {
    errors.yearsOfRegularResidence = "Indiquez votre durée de résidence régulière.";
  }
  return errors;
}

export default function Allocs() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [errors, setErrors] = useState({});
  const [results, setResults] = useState(null);
  const [apiError, setApiError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
    setErrors((current) => ({ ...current, [name]: undefined }));
  };

  const handleBoolean = (name, value) => {
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const nextErrors = validate(form);
    if (Object.keys(nextErrors).length) {
      setErrors(nextErrors);
      return;
    }

    setLoading(true);
    setApiError("");
    try {
      const response = await fetch("/api/v1/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(buildPayload(form)),
      });
      const data = await response.json().catch(() => null);
      if (!response.ok) throw new Error(data?.detail || "Le service d’éligibilité est indisponible.");
      setResults(data.user_eligible_benefits);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (error) {
      setApiError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResults(null);
    setApiError("");
  };

  return (
    <div className="page">
      <header className="header">
        <div className="header-inner">
          <div className="logo-badge"><span className="logo-dot">E</span> Eligy</div>
          <h1>Découvrez les aides adaptées à votre situation.</h1>
          <p>Une estimation simple, gratuite et sans création de compte.</p>
        </div>
      </header>

      <main className="main">
        <div className="card">
          {results ? (
            <section className="results" aria-live="polite">
              <p className="eyebrow">Votre estimation</p>
              <h2>Résultats d’éligibilité</h2>
              <p className="disclaimer">Cette estimation est indicative et ne remplace pas l’étude de votre dossier par l’organisme concerné.</p>
              <div className="benefit-list">
                {results.map((benefit) => (
                  <article className={`benefit ${benefit.eligible ? "eligible" : "ineligible"}`} key={benefit.benefit_name}>
                    <div className="benefit-heading">
                      <h3>{benefit.benefit_name}</h3>
                      <span>{benefit.eligible ? "Potentiellement éligible" : "Non éligible"}</span>
                    </div>
                    <details>
                      <summary>Voir le détail des critères</summary>
                      <ul>
                        {benefit.criteria_details.map((criterion) => (
                          <li key={criterion.criterion_name} className={criterion.status ? "pass" : "fail"}>
                            <span aria-hidden="true">{criterion.status ? "✓" : "×"}</span>
                            {criterion.criterion_name.replace(/^\[[^\]]+\]\s*/, "")}
                          </li>
                        ))}
                      </ul>
                    </details>
                    {benefit.eligible && BENEFIT_ACTION_URLS[benefit.benefit_name] && (
                      <a
                        className="benefit-action"
                        href={BENEFIT_ACTION_URLS[benefit.benefit_name]}
                        target="_blank"
                        rel="noreferrer"
                      >
                        Débuter les démarches <span aria-hidden="true">↗</span>
                      </a>
                    )}
                  </article>
                ))}
              </div>
              <button className="btn-secondary" type="button" onClick={reset}>Modifier mes réponses</button>
            </section>
          ) : (
            <form onSubmit={handleSubmit} noValidate>
              <p className="eyebrow">Simulation personnalisée</p>
              <h2>Votre situation</h2>
              <p className="card-subtitle">Tous les montants demandés sont mensuels.</p>

              <section className="form-section">
                <h3>Identité et résidence</h3>
                <div className="form-grid">
                  <NumberField name="age" label="Votre âge" value={form.age} onChange={handleChange} max={120} suffix="ans" error={errors.age} />
                  <div className="field">
                    <label htmlFor="nationalityZone">Votre nationalité</label>
                    <select id="nationalityZone" name="nationalityZone" value={form.nationalityZone} onChange={handleChange}>
                      <option value="FR">Française</option>
                      <option value="UE_EEE_CH">Union européenne, EEE ou Suisse</option>
                      <option value="OTHER">Autre</option>
                    </select>
                  </div>
                  <div className="field">
                    <label htmlFor="countryOfResidence">Pays de résidence</label>
                    <select id="countryOfResidence" name="countryOfResidence" value={form.countryOfResidence} onChange={handleChange}>
                      <option value="FR">France</option>
                      <option value="OTHER">Autre pays</option>
                    </select>
                  </div>
                  <NumberField name="monthsInFrancePerYear" label="Présence en France par an" value={form.monthsInFrancePerYear} onChange={handleChange} max={12} suffix="mois" error={errors.monthsInFrancePerYear} />
                  <NumberField name="monthsOfStableResidence" label="Résidence stable en France" value={form.monthsOfStableResidence} onChange={handleChange} suffix="mois" error={errors.monthsOfStableResidence} />
                  {form.nationalityZone === "OTHER" && (
                    <NumberField name="yearsOfRegularResidence" label="Résidence régulière en France" value={form.yearsOfRegularResidence} onChange={handleChange} suffix="ans" error={errors.yearsOfRegularResidence} />
                  )}
                </div>
                <YesNoField name="isDetachedWorker" label="Êtes-vous travailleur détaché ?" value={form.isDetachedWorker} onChange={handleBoolean} />
                {form.nationalityZone !== "FR" && <YesNoField name="hasStableResidenceRight" label="Disposez-vous d’un droit au séjour valide ?" value={form.hasStableResidenceRight} onChange={handleBoolean} />}
                {form.nationalityZone === "OTHER" && (
                  <>
                    <YesNoField name="hasWorkPermittingVisa" label="Votre titre de séjour autorise-t-il à travailler ?" value={form.hasWorkPermittingVisa} onChange={handleBoolean} />
                    <YesNoField name="hasResidentCard" label="Possédez-vous une carte de résident ?" value={form.hasResidentCard} onChange={handleBoolean} />
                    <YesNoField name="isRefugeeOrProtected" label="Êtes-vous réfugié(e) ou bénéficiaire d’une protection subsidiaire ?" value={form.isRefugeeOrProtected} onChange={handleBoolean} />
                    <YesNoField name="isStateless" label="Êtes-vous reconnu(e) apatride ?" value={form.isStateless} onChange={handleBoolean} />
                  </>
                )}
              </section>

              <section className="form-section">
                <h3>Activité et ressources</h3>
                <div className="field">
                  <label htmlFor="currentStatus">Situation actuelle</label>
                  <select id="currentStatus" name="currentStatus" value={form.currentStatus} onChange={handleChange}>
                    {STATUS_OPTIONS.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
                  </select>
                </div>
                <div className="form-grid">
                  <NumberField name="monthlyNetSocialIncome" label="Revenu net social personnel" value={form.monthlyNetSocialIncome} onChange={handleChange} suffix="€" error={errors.monthlyNetSocialIncome} />
                  <NumberField name="householdTotalResources" label="Ressources totales du foyer" value={form.householdTotalResources} onChange={handleChange} suffix="€" error={errors.householdTotalResources} />
                </div>
              </section>

              <section className="form-section">
                <h3>Famille</h3>
                <div className="form-grid">
                  <NumberField name="dependentChildrenCount" label="Nombre d’enfants à charge" value={form.dependentChildrenCount} onChange={handleChange} error={errors.dependentChildrenCount} />
                  {Number(form.dependentChildrenCount) > 0 && <NumberField name="childrenMaxAge" label="Âge de l’enfant le plus âgé" value={form.childrenMaxAge} onChange={handleChange} max={30} suffix="ans" error={errors.childrenMaxAge} />}
                </div>
                <YesNoField name="isIsolatedParentWithChildUnder3" label="Êtes-vous parent isolé avec un enfant de moins de 3 ans ?" value={form.isIsolatedParentWithChildUnder3} onChange={handleBoolean} />
              </section>

              {apiError && <div className="api-error" role="alert">{apiError} Vérifiez que l’API est démarrée.</div>}
              <button className="btn-submit" type="submit" disabled={loading}>{loading ? "Analyse en cours…" : "Vérifier mes droits →"}</button>
            </form>
          )}
        </div>
      </main>
      <footer className="footer">© 2026 Eligy — Estimation indicative des droits sociaux</footer>
    </div>
  );
}
