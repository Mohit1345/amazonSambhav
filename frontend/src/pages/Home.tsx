import { ArrowRight, FileSearch } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    exportCountry: "",
    importCountry: "",
    product: "",
  });

  const countries = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "American Samoa",
    "Andorra",
    "Angola",
    "Anguilla",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Aruba",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bermuda",
    "Bhutan",
    "Bolivia (Plurinational State of)",
    "Bosnia and Herzegovina",
    "Botswana",
    "Bouvet Island",
    "Brazil",
    "British Indian Ocean Territory",
    "Brunei Darussalam",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cabo Verde",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Cayman Islands",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Christmas Island",
    "Cocos (Keeling) Islands",
    "Colombia",
    "Comoros",
    "Congo",
    "Congo, Democratic Republic of",
    "Cook Islands",
    "Costa Rica",
    "Côte d'Ivoire",
    "Croatia",
    "Cuba",
    "Curacao",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Eswatini",
    "Ethiopia",
    "Falkland Islands (Malvinas)",
    "Faroe Islands",
    "Fiji",
    "Finland",
    "France",
    "French Guiana",
    "French Polynesia",
    "French Southern territories",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Gibraltar",
    "Greece",
    "Greenland",
    "Grenada",
    "Guam",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Heard and McDonald Islands",
    "Honduras",
    "Hong Kong, China Special Administrative Region",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran (Islamic Republic of)",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Korea, Democratic People's Republic of",
    "Korea, Republic of",
    "Kosovo",
    "Kuwait",
    "Kyrgyzstan",
    "Lao, People's Democratic Republic",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Macao, China Special Administrative Region",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Mauritania",
    "Mauritius",
    "Mayotte",
    "Mexico",
    "Micronesia (Federated States of)",
    "Midway Islands",
    "Moldova, Republic of",
    "Mongolia",
    "Montenegro",
    "Montserrat",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "New Caledonia",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "Niue",
    "Norfolk Island",
    "North Macedonia, Republic of",
    "Northern Mariana Islands",
    "Norway",
    "Oman",
    "Pacific Islands",
    "Pakistan",
    "Palau",
    "Palestine, State of",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Pitcairn",
    "Poland",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "Romania",
    "Russian Federation",
    "Rwanda",
    "Saint Helena",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Pierre and Miquelon",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Georgia and the South Sandwich Islands",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Svalbard and Jan Mayen Islands",
    "Sweden",
    "Switzerland",
    "Syrian Arab Republic",
    "Taipei, Chinese",
    "Tajikistan",
    "Tanzania, United Republic of",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tokelau",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Türkiye",
    "Turkmenistan",
    "Turks and Caicos Islands",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States Minor Outlying Islands",
    "United States of America",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Venezuela (Bolivarian Republic of)",
    "Viet Nam",
    "Virgin Islands, British",
    "Virgin Islands, United States",
    "Wallis and Futuna",
    "Western Sahara",
    "Yemen",
    "Zambia",
    "Zimbabwe",
  ];

  const handleSubmit = async(e: React.FormEvent) => {
    e.preventDefault(); // Prevent default form submission behavior

    const requestData = {
      product_name:formData.product,
      import_country: formData.importCountry, // Using "destinationCountry" as export country
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/submit-product", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (response.ok) {
        const responseData = await response.json();
        console.log("API Response:", responseData);
        localStorage.setItem("amazon",JSON.stringify(responseData))
        navigate("/results");
        alert("Data submitted successfully!");
      } else {
        console.error("API Error:", response.statusText);
        alert("Failed to submit data. Please try again.");
      }
    } catch (error) {
      console.error("Network Error:", error);
      alert("Network error. Please check your connection.");
    }
   
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Global Trade Compliance Made Simple
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Get instant access to export regulations, compliance requirements, and
          available incentives for international trade.
        </p>
      </div>

      <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-md overflow-hidden p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label
              htmlFor="exportCountry"
              className="block text-sm font-medium text-gray-700"
            >
              Export Country
            </label>
            <select
              id="exportCountry"
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              value={formData.exportCountry}
              onChange={(e) =>
                setFormData((prev) => ({
                  ...prev,
                  exportCountry: e.target.value,
                }))
              }
            >
              {countries.map((country) => (
                <option key={country} value={country}>
                  {country}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label
              htmlFor="importCountry"
              className="block text-sm font-medium text-gray-700"
            >
              Import Country
            </label>
            <select
              id="exportCountry"
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              value={formData.importCountry}
              onChange={(e) =>
                setFormData((prev) => ({
                  ...prev,
                  importCountry: e.target.value,
                }))
              }
            >
              {countries.map((country) => (
                <option key={country} value={country}>
                  {country}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label
              htmlFor="product"
              className="block text-sm font-medium text-gray-700"
            >
              Product
            </label>
            <input
              type="text"
              id="product"
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              value={formData.product}
              onChange={(e) =>
                setFormData((prev) => ({ ...prev, product: e.target.value }))
              }
            />
          </div>

          <button
            type="submit"
            className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-blue-600 hover:bg-blue-700"
          >
            Get Compliance Info <ArrowRight className="ml-2 h-5 w-5" />
          </button>
        </form>
      </div>

      <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="text-center p-6">
          <FileSearch className="h-12 w-12 text-blue-600 mx-auto" />
          <h3 className="mt-4 text-xl font-semibold">Comprehensive Analysis</h3>
          <p className="mt-2 text-gray-600">
            Get detailed compliance requirements and documentation needs
          </p>
        </div>
        <div className="text-center p-6">
          <FileSearch className="h-12 w-12 text-blue-600 mx-auto" />
          <h3 className="mt-4 text-xl font-semibold">Available Incentives</h3>
          <p className="mt-2 text-gray-600">
            Discover grants and incentives for your exports
          </p>
        </div>
        <div className="text-center p-6">
          <FileSearch className="h-12 w-12 text-blue-600 mx-auto" />
          <h3 className="mt-4 text-xl font-semibold">Expert Support</h3>
          <p className="mt-2 text-gray-600">
            Get assistance from our AI-powered chatbot
          </p>
        </div>
      </div>
    </div>
  );
}
