import { Check } from 'lucide-react'
import { useState } from 'react'
import { useLocation } from 'react-router-dom'
import Chat from '../components/Chat'

const dummyData = [
  {
    "title": "Amazon Product Compliance",
    "introduction": "This section details the mandatory and recommended requirements for ensuring your Notebooks comply with Amazon's product compliance policies. Adherence to these guidelines is crucial for successful export and avoiding penalties.",
    "Mandatory Requirements": [
      "Product Labeling: Exporters must adhere to labeling norms, including Country of Origin, Statement of content, and Declaration of responsibility (manufacturer, packer, or distributor information).",
      "Product Safety: Manufacturers/distributors must guarantee product safety and harmlessness. Any usage warnings must be clearly stated on the product label."
    ],
    "Recommended Requirements": [
      "Implement a quality control process to ensure consistent product quality.",
      "Provide clear and detailed product descriptions to avoid customer confusion and potential returns."
    ],
    "Other important check points": [
      "Verify that all labeling requirements are met before exporting the product.",
      "Ensure product safety is a priority throughout the manufacturing and distribution process.",
      "Consult the provided links for detailed information on labeling and product safety regulations."
    ]
  },
  {
    "title": "Import Compliance for Notebooks",
    "introduction": "This section details the mandatory and recommended requirements for importing notebooks, ensuring compliance with relevant regulations and maximizing the chances of a smooth import process.",
    "Mandatory Requirements": [
      "Obtain necessary import licenses and permits.",
      "Comply with customs documentation requirements."
    ],
    "Recommended Requirements": [
      "Conduct a thorough review of import regulations for the destination country.",
      "Engage with a customs broker to facilitate the import process."
    ],
    "Other important check points": [
      "Verify all labeling requirements are met, including country of origin, material composition, and any necessary warnings or care instructions.",
      "Confirm that the notebooks meet all relevant safety standards for their intended use. This may include testing by accredited laboratories.",
      "Ensure compliance with all applicable import regulations and tariffs of the destination country."
    ]
  },
  {
    "title": "Export Compliance for Notebooks",
    "introduction": "This section details the mandatory and recommended requirements for ensuring compliance when exporting Notebooks, focusing on adherence to regulations and best practices to avoid delays or rejection of shipments.",
    "Mandatory Requirements": [
      "Obtain required export licenses and permits.",
      "Comply with export documentation requirements."
    ],
    "Recommended Requirements": [
      "Implement an export compliance program.",
      "Stay updated on changes in export regulations."
    ],
    "Other important check points": [
      "Verify all labeling requirements are met according to the destination country's regulations. Note that these requirements may vary widely based on the specific composition and intended use of the Notebook.",
      "Confirm that any necessary testing and certifications have been obtained before shipment. This may include safety testing relevant to materials used in the Notebook.",
      "Maintain thorough and accurate records of all compliance documentation, including test results, certifications, and labeling information. These records are critical for demonstrating compliance to regulatory bodies if necessary."
    ]
  },
  {
    "title": "Taxation and Incentives",
    "introduction": "This section details the tax implications and potential incentives associated with exporting Notebooks, ensuring compliance and maximizing profitability.",
    "Benefits": [
      "Potential tax deductions for export-related expenses",
      "Possible export incentives offered by the government",
      "Opportunity to claim duty drawback on imported materials used in exported products"
    ]
  }
]

const ChecklistItem = ({ id, label, checked, onCheckedChange }) => (
  <div className="flex items-center space-x-3">
    <div 
      className="relative w-6 h-6 cursor-pointer"
      onClick={() => onCheckedChange(!checked)}
    >
      <input
        type="checkbox"
        id={id}
        checked={checked}
        onChange={() => {}}
        className="sr-only"
      />
      <div className={`w-6 h-6 border-2 rounded-md transition-colors ${checked ? 'bg-green-500 border-green-500' : 'border-gray-300'}`}></div>
      {checked && (
        <Check className="absolute top-0.5 left-0.5 text-white w-5 h-5" />
      )}
    </div>
    <label
      htmlFor={id}
      className="text-sm font-medium text-gray-700 cursor-pointer select-none"
      onClick={() => onCheckedChange(!checked)}
    >
      {label}
    </label>
  </div>
)

export default function Results() {
  const location = useLocation()
  const { exportCountry, importCountry, product } = location.state || {}
  const [checklist, setChecklist] = useState({})

  const handleChecklistChange = (id, isChecked) => {
    setChecklist(prev => ({ ...prev, [id]: isChecked }))
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 relative min-h-screen pb-24 bg-gradient-to-b from-gray-50 to-white">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Compliance Checklist</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {dummyData.map((item, index) => (
          <div key={index} className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">{item.title}</h2>
            <p className="text-gray-600 mb-6">{item.introduction}</p>
            {['Mandatory Requirements', 'Recommended Requirements', 'Benefits'].map((section) => {
              if (item[section] && item[section].length > 0 && item[section][0] !== "information not available") {
                return (
                  <div key={section} className="mb-6">
                    <h3 className="text-lg font-medium text-gray-700 mb-3">{section}</h3>
                    <div className="space-y-3">
                      {item[section].map((requirement, idx) => (
                        <ChecklistItem
                          key={`${index}-${section}-${idx}`}
                          id={`${index}-${section}-${idx}`}
                          label={requirement}
                          checked={checklist[`${index}-${section}-${idx}`] || false}
                          onCheckedChange={(isChecked) => handleChecklistChange(`${index}-${section}-${idx}`, isChecked)}
                        />
                      ))}
                    </div>
                  </div>
                )
              }
              return null
            })}
            {item["Other important check points"] && (
              <div className="mt-6">
                <h3 className="text-lg font-medium text-gray-700 mb-3">Other Important Check Points</h3>
                <ul className="list-disc list-inside space-y-2 text-gray-600">
                  {item["Other important check points"].map((point, idx) => (
                    <li key={idx}>{point}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
      <Chat />
    </div>
  )
}

