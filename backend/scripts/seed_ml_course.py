"""
One-time bulk seed script: loads the full "Machine Learning" course
(9 modules, 52 lessons + 1 capstone assignment) into MongoDB, including
REAL Google Slides (PPT) and Google Colab links pulled from the hyperlinks
embedded in ML.xlsx.

HOW TO RUN (from your own computer, not Streamlit Cloud):

    pip install pymongo
    export MONGO_URI="mongodb+srv://<your_db_user>:<your_db_password>@<your_cluster>.mongodb.net/?retryWrites=true&w=majority"
    python seed_ml_course.py

SAFE TO RE-RUN: it upserts by title, so running it twice won't create
duplicate courses/modules/lessons — it will just refresh the links.

NOTE: some lessons genuinely have no PPT or no Colab notebook in the
source file (e.g. practical-demo lessons whose "code" link is actually a
Google Drive file instead of Colab, or concept-only lessons with no code
at all) — those fields are left as "" on purpose, not missing data.
"""

import os
import sys

from pymongo import MongoClient
from pymongo.server_api import ServerApi

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME", "dsiar_lms")

if not MONGO_URI:
    print("ERROR: set the MONGO_URI environment variable first.")
    sys.exit(1)

client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
db = client[DB_NAME]

COURSE = {
    "title": "Machine Learning",
    "category": "Machine Learning",
    "description": (
        "Learn Machine Learning from the ground up — data preprocessing, "
        "supervised and unsupervised learning, dimensionality reduction, "
        "ensemble methods, and advanced topics like time series, "
        "recommendation systems, and explainable AI — all with hands-on "
        "Python demos and a real-world capstone project."
    ),
    "thumbnail_url": "",
    "is_free": True,
}

MODULES = [
    ("Introduction to Machine Learning", [
        ("Introduction to Machine Learning", "zc6D6IJf2Ro", "https://docs.google.com/presentation/d/144yF2mhzLQ7UBh5za8zWenY-Fgep7-cI/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Types of Machine Learning", "V_FZ9QsUgCE", "https://docs.google.com/presentation/d/1oi1NNZXtmNohk5Wat4dsmf8-xPwewKz1/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Steps in the Machine Learning Workflow", "2ejDU-FMC4I", "https://docs.google.com/presentation/d/1MmFojPJtOSJSNBzhVMGAPJ0QFtTC1Dg6/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Introduction to Python Libraries for ML", "0yoVZfwbazE", "https://docs.google.com/presentation/d/1d1HBri2SMXFAjDtzgB1Y4PwHWhhysP93/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
    ]),
    ("Data Preprocessing", [
        ("Introduction to Data Preprocessing", "P8wLBszQj6Y", "https://docs.google.com/presentation/d/1r8RcVYvwi2svpNjv0RYZMTyJekN1cZMw/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Understanding Data and Features", "8va2qo5YRho", "https://docs.google.com/presentation/d/1JcskPGQtZ1-bqtIyVSW6Aap6IbT0Kufc/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Handling Missing Data", "GrF1RJmEqYg", "https://docs.google.com/presentation/d/1KAX1jHzpcFltMEczD286k5cQU5KphYnv/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Normalization & Standardization", "4rBcm0qyNEY", "https://docs.google.com/presentation/d/19QiEenSJZtAp1M24r_gL8ygGTVfEJcve/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1EqNgiXJN3TJH2XBdLel-MJm50WNtlTCS?usp=drive_link"),
        ("Encoding Categorical Data", "ZNxReutNPdw", "https://docs.google.com/presentation/d/1WMcPwbf_ccT-7vXMvEq5y-OCdCUTFlc9/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/15cITOlX9HiUakkwoZvcpLAock6a-4EVV?usp=drive_link"),
        ("Feature Engineering & Feature Selection", "D4yKsosAC9M", "https://docs.google.com/presentation/d/18nNdCF0kSPo1XCbwxi7RI6RDymjnRUUA/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Train-Test Split & Cross-Validation", "CwvCVszArIE", "https://docs.google.com/presentation/d/15M0dCse8QAopdBq_QMUvyLwUYO98vrc_/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
    ]),
    ("Supervised Learning", [
        ("Loss Functions & Gradient Descent | Supervised Learning", "tuaoS4JPwds", "https://docs.google.com/presentation/d/1Dyym-IA23GzkzMZDzHk85PrHP2r387Tp/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Linear & Polynomial Regression | Supervised Learning", "XzerqaVuoco", "https://docs.google.com/presentation/d/1XwgMXWh_iy3LdktwmpksEhp7CvOul-x3/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Linear, Polynomial & Multiple Linear Regression – Practical Python Demo", "7hLEKbMZprU", "", "https://drive.google.com/file/d/1VHEHEY_w4VkIjl4USdQWjSrmkUkyO9Eb/view?usp=drive_link"),
        ("Regularization in Machine Learning | L1 & L2 Explained | Supervised Learning", "BM2c7_enSRo", "https://docs.google.com/presentation/d/1-lGH94nlKDkl56PYDiWgwT4M9BCw87pH/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Ridge & Lasso Regression – Practical Python Demo | Regularization L1 & L2", "kkUc6Yei_C4", "", "https://drive.google.com/file/d/1996v8DcHk0pR8h69OoFeW4NHNBXU07Ai/view?usp=drive_link"),
        ("Evaluation Metrics in Machine Learning | Supervised Learning", "9Pzo9sAKu-Y", "https://docs.google.com/presentation/d/1btGsIuS4wnPtMv9_4V9R8VarXY5mDn5W/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1Y3rxovT6IEtgf58kNAdtG7l3JjGK1qUF?usp=drive_link"),
        ("Logistics Regression | Classification in Machine Learning", "9Pzo9sAKu-Y", "https://docs.google.com/presentation/d/1gVyGOnh3zpU6KhmqB6B1CDN80oOB3AZc/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1E1ZToUVO-GjfRZrnv6Dmsv-9IskcMtFy?usp=drive_link"),
        ("Decision Trees & Random Forests | Classification in Machine Learning", "Qse4vEJqVuA", "https://docs.google.com/presentation/d/1bzUkW40pkPs1qML3wgumjwt-1CbNj7Db/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Decision Tree & Random Forest – Practical Python Demo", "2gvn6QxwtdY", "", "https://colab.research.google.com/drive/1x1tZnMR7XXE8eptBoymv-33J_2tRCM2P?usp=drive_link"),
        ("Support Vector Machines (SVM) | Theory & Intuition", "PBErv_8GXAs", "https://docs.google.com/presentation/d/17gfUNaCw48C8Qnm4cU_yLsQGiHw3Xdz9/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Support Vector Machines (SVM) - Practical Python Demo", "E5NOPukOy3Y", "", "https://colab.research.google.com/drive/19UAmBWmMvQIWIH1k4sdAGPwOBUK2um1Z?usp=drive_link"),
        ("Naive Bayes Classifier", "oIn9hlT0HB4", "https://docs.google.com/presentation/d/1wLiFXfrPABQQvSVIiAZKEY7hiNqf5aNa/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1zc4M_aEPZ1D3rj9ewb6cK6eanuh1_sdY?usp=drive_link"),
        ("Classification Evaluation Metrics | Accuracy, Precision, Recall, F1-Score, ROC, AUC", "-NV3NdivvZc", "https://docs.google.com/presentation/d/1KRMsn9yYiPnMuBvQRjONK8qfAz3Cbv17/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1c4rFmLgEPvfsOMI7vUHnBj4lc1SvIS-E?usp=sharing"),
    ]),
    ("Unsupervised Learning: Clustering", [
        ("Introduction to Clustering | Unsupervised Learning", "E8METAEzxco", "https://docs.google.com/presentation/d/19tMwZDgq49IjSbrx9XaszaQHrSHfpmAZ/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("K-Means Clustering | Unsupervised Learning", "Dn-6KllVqto", "https://docs.google.com/presentation/d/19duH94aGtNMPSBIRgTuLw5ucDKRQpYjK/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1K29qiaNfIDBVdaW66RfYLvB2OYV-LLNC?usp=sharing"),
        ("Hierarchical Clustering | Unsupervised Learning", "Tqebrskw1vc", "https://docs.google.com/presentation/d/1Gm6q5wfzg1TpHatRjECqm_cG1MI1-hxY/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/18DuqOdyiPG-AvkKGa1Ddw7ItRvSxcOt7?usp=sharing"),
        ("DBSCAN Clustering | Density-Based Clustering| Unsupervised Learning", "Peh6BZ5CgK8", "https://docs.google.com/presentation/d/10-BJN9gSuWUtm5XRoaV0xjyAJsLgM6-U/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/14ACmGhGrvGFPhn3K8v2YTJuGck-g5fxP?usp=sharing"),
        ("Clustering Evaluation Metrics | Silhouette Score, Davies–Bouldin | Unsupervised Learning", "7RPUawLY5LI", "https://docs.google.com/presentation/d/17DtaiEYuLUNiJR5X36ln4EdHVdJT_fKo/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1j8AYzleTPxpEJ_kNZeX_Z9tODKerXcBX?usp=sharing"),
    ]),
    ("Dimensionality Reduction", [
        ("Introduction to Dimensionality Reduction", "TedrllS78kc", "https://docs.google.com/presentation/d/1AD19Pbr7zgS4FvXJku-VtVi5_Lns6fUr/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Principal Component Analysis (PCA) | Theory & Intuition | Dimensionality Reduction", "bAZjpOwfUaA", "https://docs.google.com/presentation/d/1YgtznkhQMUKT2DP__d3das-EupM8DHjL/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("PCA Practical Demo | Principal Component Analysis in Python | Dimensionality Reduction", "z-3H-1sEe-M", "", "https://colab.research.google.com/drive/1NM-i9CmcXyCZz2fHURxtwRaLA15hQxvS?usp=sharing"),
        ("Singular Value Decomposition (SVD) | Dimensionality Reduction", "1_2dNXjTDkc", "https://docs.google.com/presentation/d/1gRkzNG65tXAVXlJEbt3tLzCZrhaRSD1E/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1kS_uCPE4XXtfIk6ffSR-vfvsZJzTFmo-?usp=sharing"),
        ("t-SNE | Dimensionality Reduction", "tVcEbDDrqek", "https://docs.google.com/presentation/d/1qZNzuNKULFWnqiHx454VQ0KEiUFyvQae/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1Th-BDUTBKrlEgsTqdJly7MkKaHnIfvRC?usp=sharing"),
    ]),
    ("Ensemble Learning", [
        ("Introduction to Ensemble Learning", "xN0xHo7y774", "https://docs.google.com/presentation/d/15gup2okNxlbn58xkC-0zj8IqD2ZL7OAW/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Bagging & Random Forest (Theory) | Ensemble Learning", "LCBekWXjAtw", "https://docs.google.com/presentation/d/1yYMsU7sT_uECIM-8lN-SZEC6rQ0Rq-L4/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Bagging & Random Forest (Practical) | Ensemble Learning", "2-ixpLi8rpo", "", "https://drive.google.com/file/d/1XrrFKlXL5w8E5BwWW9cQvTIzAZPeGHS2/view?usp=sharing"),
        ("Boosting Techniques | AdaBoost, Gradient Boosting, XGBoost (Concepts)  | Ensemble Learning", "J29WCC_RkBQ", "https://docs.google.com/presentation/d/1xOFwwjdu0WZGiEjRFM_yIoDItD9CajTR/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Boosting Techniques | AdaBoost, Gradient Boosting, XGBoost (Practical)  | Ensemble Learning", "CfNeZjbSOac", "", "https://colab.research.google.com/drive/1qGW18G2I9GKEg3lhQAMXed8dnFGZXqK-?usp=sharing"),
        ("Stacking Models | Ensemble Learning | Theory + Python Demo", "BnkxmdFA7RM", "https://docs.google.com/presentation/d/10ap59qbdJRAh2F4ednOOAIkai_QLUsRT/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1Zrs4Abje_iPMmpi2q6PEv8VpFPfcfeks?usp=sharing"),
    ]),
    ("Advanced Topics", [
        ("Handling Imbalanced Data | SMOTE & Weighted Loss Functions (Theory) | Advanced Topics", "crL29obx7Ok", "https://docs.google.com/presentation/d/1XgTN5mP4F-PY3m3FQNSQvdwcu1tGMBtU/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Handling Imbalanced Data | SMOTE & Weighted Loss Functions (Practical) | Advanced Topics", "w9glEIlZrMI", "", "https://colab.research.google.com/drive/1g5n9prVNKt3vm_Mh0a_y_iKrzkB15LB-?usp=sharing"),
        ("Time Series Analysis | Theory & Concepts | Advanced Topics", "mXrPw8riXOU", "https://docs.google.com/presentation/d/1898ZyCcCwjnNrEoI10h88P4zTo8KcMvu/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Time Series Forecasting | ARIMA & SARIMA | Practical Python Demo | Advanced Topics", "FPgl8wdjyJU", "", "https://colab.research.google.com/drive/1WMhejC1O4P9GpW4KJQIxFbpYah_saSDm?usp=sharing"),
        ("Recommendation Systems | Theory & Concepts | Advanced Topics", "RtVm55GMkGo", "https://docs.google.com/presentation/d/1uGGTxeliYmtC4eyAatGYbhi5DnL8H8eL/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Recommendation Systems | Practical Python Demo | Advanced Topics", "hlPo4fTzmyg", "", "https://colab.research.google.com/drive/1cdw-pPNHF6YGGgjtJKbwoBqA4tsdo9IL?usp=sharing"),
        ("Model Deployment in Machine Learning | Theory & Concepts | Advanced Topics", "K3EqSCITqsk", "https://docs.google.com/presentation/d/1mC1ZsbabwbkTxQCKt_IAGzVRHlZIbyTY/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Model Deployment – Saving & Loading ML Models | Joblib & Pickle | Advanced Topics", "NHF1fS6Zhv0", "", "https://colab.research.google.com/drive/1-9pxjIk1rbVAB5o70JwzhOdTgArEg1VN?usp=sharing"),
    ]),
    ("Explainability and Ethics", [
        ("Explainable AI (XAI) | SHAP & LIME | Theory + Practical Demo | Explainability and Ethics", "E62uhyai74k", "https://docs.google.com/presentation/d/1reKIzsFpmDNgMJmvavPkd4SZpVp-ZKrE/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1uxuvDLyfsLRM_fX0-82wuVDp6uvx59aQ?usp=sharing"),
        ("Ethical AI & ML Regulations | Bias, Privacy, Fairness, GDPR | | Explainability and Ethics", "Iql_rgjQd4c", "https://docs.google.com/presentation/d/13HzsXJEJQi8cPthkM68onJH_dvuz8z2F/edit?usp=sharing&ouid=115205148767082075498&rtpof=true&sd=true", ""),
    ]),
    ("Capstone Project: Customer Churn Prediction", [
        ("Customer Churn Prediction - Part I | Capstone Project", "LD6a4H8wxhQ", "", "https://colab.research.google.com/drive/1rjhzBXGj5G58DlEw-bvsI8RVennBPAG3?usp=sharing"),
        ("Customer Churn Prediction - Part II | Capstone Project", "66vxwFHqg94", "", "https://colab.research.google.com/drive/1rjhzBXGj5G58DlEw-bvsI8RVennBPAG3?usp=sharing"),
    ]),
]
CAPSTONE_ASSIGNMENT_TITLE = "Capstone Project Assignment"
CAPSTONE_ASSIGNMENT_DESC = (
    "Build a Customer Churn Prediction project following the capstone "
    "module: load and preprocess the dataset, train and evaluate a "
    "classification model, and summarize your findings. Submit a link to "
    "your GitHub repo or notebook."
)


def upsert_course():
    existing = db.courses.find_one({"title": COURSE["title"]})
    if existing:
        db.courses.update_one({"_id": existing["_id"]}, {"$set": COURSE})
        return existing["_id"]
    COURSE["order"] = db.courses.count_documents({}) + 1
    result = db.courses.insert_one(COURSE)
    return result.inserted_id


def upsert_module(course_id, title, order):
    existing = db.modules.find_one({"course_id": str(course_id), "title": title})
    if existing:
        return existing["_id"]
    result = db.modules.insert_one({"course_id": str(course_id), "title": title, "order": order})
    return result.inserted_id


def upsert_lesson(module_id, title, order, youtube_id, ppt_link, colab_link):
    existing = db.lessons.find_one({"module_id": str(module_id), "title": title})
    doc = {
        "module_id": str(module_id),
        "title": title,
        "order": order,
        "youtube_id": youtube_id,
        "ppt_link": ppt_link,
        "colab_link": colab_link,
        "dataset_link": "",
    }
    if existing:
        db.lessons.update_one({"_id": existing["_id"]}, {"$set": doc})
    else:
        db.lessons.insert_one(doc)


def upsert_capstone_assignment(course_id):
    existing = db.assignments.find_one({"course_id": str(course_id), "title": CAPSTONE_ASSIGNMENT_TITLE})
    if existing:
        return
    db.assignments.insert_one(
        {
            "course_id": str(course_id),
            "title": CAPSTONE_ASSIGNMENT_TITLE,
            "description": CAPSTONE_ASSIGNMENT_DESC,
            "due_date": "",
        }
    )


def main():
    course_id = upsert_course()
    print(f"Course ready: {COURSE['title']} ({course_id})")

    for m_order, (module_title, lessons) in enumerate(MODULES, start=1):
        module_id = upsert_module(course_id, module_title, m_order)
        print(f"  Module {m_order}: {module_title} ({module_id})")
        for l_order, (lesson_title, youtube_id, ppt_link, colab_link) in enumerate(lessons, start=1):
            upsert_lesson(module_id, lesson_title, l_order, youtube_id, ppt_link, colab_link)
            print(f"    Lesson {l_order}: {lesson_title}")

    upsert_capstone_assignment(course_id)
    print("Capstone assignment ready.")
    print("\nDone! Reload the LMS and check the Course Catalog.")


if __name__ == "__main__":
    main()
