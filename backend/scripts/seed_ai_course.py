"""
One-time bulk seed script: loads the full "Artificial Intelligence" course
(10 modules, 39 lessons + 1 capstone assignment) into MongoDB, including
REAL Google Slides (PPT) and Google Colab links pulled from the hyperlinks
embedded in AI.xlsx.

HOW TO RUN (from your own computer, not Streamlit Cloud):

    pip install pymongo
    export MONGO_URI="mongodb+srv://karkavelrajaj_db_user:YOUR_PASSWORD@cluster0.ua3bzky.mongodb.net/?retryWrites=true&w=majority"
    python seed_ai_course.py

SAFE TO RE-RUN: it upserts by title, so running it twice won't create
duplicate courses/modules/lessons — it will just refresh the links.

NOTE: some lessons genuinely have no PPT or no Colab notebook in the
source file (e.g. concept-only lessons) — those fields are left as ""
on purpose, not missing data.
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
    "title": "Artificial Intelligence",
    "category": "Artificial Intelligence",
    "description": (
        "Learn AI from fundamentals to advanced topics, including machine "
        "learning, deep learning, NLP, and computer vision. Gain hands-on "
        "experience with real-world projects and ethical AI practices."
    ),
    "thumbnail_url": "https://raw.githubusercontent.com/karkavelrajaj-coder/dsiar-lms/main/assets/AI%20Thumbnail.png",
    "is_free": True,
}

# Each module: (module title, [ (lesson title, youtube_id, ppt_link, colab_link), ... ])
MODULES = [
    ("Introduction to AI", [
        ("Introduction to Artificial Intelligence", "OH_jd-WmSC8", "https://docs.google.com/presentation/d/1bBRCVpeh73B1130t_9o8KH17NwJ0L6UK/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
    ]),
    ("Python for AI", [
        ("Python for AI", "WBNNjEPatsg", "https://docs.google.com/presentation/d/1NS3sSTCsYOe8G7qAJxdOSMpUxYTmT9_2/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1WI2SMK3okRdwiXZK7hGeizmqp-BSovTX?usp=sharing"),
        ("Python for AI : Data Manipulation and Preprocessing", "j3QemYVHyFA", "https://docs.google.com/presentation/d/1TMVyn9AMyPSDYiJjoUwoAmGNNmZDUkXA/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1fJ-vBXcAHVwnM5evPx_JvcIt8w0swqQQ?usp=sharing"),
    ]),
    ("Machine Learning Fundamentals", [
        ("Machine Learning Fundamentals: Introduction to Machine Learning", "4nF7tKG2PN8", "https://docs.google.com/presentation/d/1amUv1SvADG47lsQHU5EaeYubwrqscGph/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Machine Learning Fundamentals: Supervised Learning: Linear Regression", "M09YSm7P3lY", "https://docs.google.com/presentation/d/1IV0rOCWWFc_WT-nLtM-kUkzrRQPLuWfB/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/15Ck724sos0dsgjJWSPo3PZ_2mKrVAKqE?usp=sharing"),
        ("Machine Learning Fundamentals: Supervised Learning: Logistic Regression", "yFglxsmjOa0", "https://docs.google.com/presentation/d/116a0OQBrt8itWW3Zrh4He1AQPE4bN0_e/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/198m5bG5U6uSu5e_RQRidcBXaZJQMsR4y?usp=sharing"),
        ("Machine Learning Fundamentals: Unsupervised Learning: Clustering", "vTZ47--_k-0", "https://docs.google.com/presentation/d/1AyW8G5WpewqmKFYaj9eR8dHZygMJ0pC1/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1NLYqOXK0X49YOWRuydgqVZGqQ3qepIYJ?usp=drive_link"),
        ("Machine Learning Fundamentals: Unsupervised Learning: PCA", "ilNogizxO4g", "https://docs.google.com/presentation/d/17tLpIZhIlr9yUDPBOb80l93KCFellMIv/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1sybo08fHI6R0asssXQboWagnCUNj71gX?usp=sharing"),
        ("Machine Learning Fundamentals: Model Evaluation", "JV6sDcwPDG0", "https://docs.google.com/presentation/d/1JCkGKrjBvB1lX1oDQXhIiv-dCE09ostR/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1vlG0Zap4irGM0tuj00MTGbo9P7ahbu1c?usp=sharing"),
        ("Machine Learning Fundamentals: Overfitting and Underfitting", "BOFmcYdE8-g", "https://docs.google.com/presentation/d/15LISbMu9-kwyGzOmqMQ9nhrNiVB7acq5/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1Er5-J442WryTmuCzVKwTs-RPSItomfQZ?usp=sharing"),
    ]),
    ("Deep Learning Fundamentals", [
        ("Deep Learning Fundamentals : Introduction to Neural Networks", "CacOPACrMUw", "https://docs.google.com/presentation/d/1Tab_QWIoTJrAFboBNEAnm1Ioo5fZZ4ym/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Deep Learning Fundamentals : Forward Propagation, Backpropagation", "eUq-API3g8w", "https://docs.google.com/presentation/d/1QrF-GpDqtOJU32WHrAqSbl6LMgJedYQ2/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Deep Learning Fundamentals : Training Neural Networks", "c_SGbpePywc", "", "https://colab.research.google.com/drive/18E5fSNxaHfdOIrttmM8M-nRcL1cNZ8A3?usp=drive_link"),
        ("Deep Learning Fundamentals : Convolution Neural Network", "CRdPyfQR0zw", "https://docs.google.com/presentation/d/1JQwdJ7bz8OAszSO9xlH8CWsDyS0J7ssz/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Deep Learning Fundamentals : Recurrent Neural Networks", "PHrcudlccsw", "https://docs.google.com/presentation/d/1nXFeHHzH11obRbAFSCh-b06SAhLpu5dU/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
    ]),
    ("Natural Language Processing", [
        ("Natural Language Processing: Basics of NLP", "I-hWqbITV6Q", "https://docs.google.com/presentation/d/1f_ebGjqG3Mma8hed2BMh1nju_XurzXXH/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Natural Language Processing: Text Preprocessing", "ZVB7EY7go-c", "https://docs.google.com/presentation/d/11UFyx9LADPqMB2drVz3Aki07Cfu7bBoz/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1H5iWzQAN88PjY-NaL2pIGXMUa9qq8ts_?usp=drive_link"),
        ("Natural Language Processing: Sentiment Analysis", "U8lQ-8Ax5QE", "https://docs.google.com/presentation/d/1GvzRBpmG9eYrY-3itcOlFO1u2ieAC-zn/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1eTMEOk0m-0Z77z2wF5bxW2BspRLpGK-g?usp=sharing"),
        ("Natural Language Processing:  Introduction to Transformers – BERT & GPT", "FgTWt4OxTOM", "https://docs.google.com/presentation/d/10ukJcGHewNSHijctBKx-Ei6UsoWiMwtj/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
    ]),
    ("Computer Vision", [
        ("Computer Vision: Basics of Image Processing", "diV_F5A2o9U", "https://docs.google.com/presentation/d/1gYofnTJR7MBs7psJlJNXu4XfORzZeqHM/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1cBMpftJ0clPEzZN9FiRlk1JOYqvAaIJN?usp=drive_link"),
        ("Computer Vision: CNNs for Vision", "niTCVnW_-Xo", "https://docs.google.com/presentation/d/1TTTTkOpAvgBKnpKN6LMw15lZNOJFhRya/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Computer Vision: CNNs for Vision - Building & Training", "xmIZl-baVu0", "https://docs.google.com/presentation/d/1obMUkt_MxdYfr39gq0av8bzRJxwGS2eR/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1eZK5MNSn_OLEHIZzgBo8Bfql8ofbHESK?usp=drive_link"),
        ("Computer Vision:  Pretrained Models (VGG & ResNet)", "3P1G5fpR_fk", "https://docs.google.com/presentation/d/1_BF1W2OiXuBO2J_uIsBVYeo4m0xyHuf3/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1w2hEONPn0IJQUntGr2A77C1bt_iusJT5?usp=sharing"),
        ("Computer Vision:  Object Detection", "venA40xi6Ic", "https://docs.google.com/presentation/d/17hhwgpKM5IoeZWqZORtgRz9V9draGudJ/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1-WyjtHqn0KEOcq3haAdPSuUQlMYVTohb?usp=drive_link"),
        ("Computer Vision:  Image Segmentation", "UFc3ZnNBD10", "https://docs.google.com/presentation/d/1Fyt0qUsCdaBQXrDCEBO0T9EKXLbhilpz/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://colab.research.google.com/drive/1PLhhz70z5dip32umurqxRVQqqfCr5pFb?usp=drive_link"),
    ]),
    ("Reinforcement Learning", [
        ("Reinforcement Learning : Basics of Reinforcement Learning", "Mgv6REWr3q8", "https://docs.google.com/presentation/d/1SEg5WuSXhBbVccUtrj8v97fgCjX8ai7K/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Reinforcement Learning : Markov Decision Processes (MDPs)", "_OCpB3qCWSM", "https://docs.google.com/presentation/d/1orTulxshh-FAMHlCsfG2MeJzZ4Bu63eE/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Q-Learning in Reinforcement Learning", "PSwI2_zvTWk", "https://docs.google.com/presentation/d/1HeH_ppOb7mWCd4U55MYxGW4AhgCLWjD7/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Deep Q-Networks (DQN) in Reinforcement Learning", "VogswKuYBcM", "https://docs.google.com/presentation/d/1l6_U3zxGaanDs_VLtacg8KqUfBTsbq6t/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
    ]),
    ("AI Ethics & Governance", [
        ("Artificial Intelligence – AI Ethics: Bias, Fairness, Accountability", "yVXH2V1HeY4", "https://docs.google.com/presentation/d/1PoP380o7MU1OibIK1Nb7tBqbCmg3V36D/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("Artificial Intelligence – Explainable AI (XAI): SHAP, LIME", "qqwJP0vYuOY", "https://docs.google.com/presentation/d/1f4y209StDxwAogkQyDGGp60awK54MgY1/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", "https://drive.google.com/file/d/1u9CmYLSeurgCiKgFyJiqL1GEeH3hbghs/view?usp=sharing"),
        ("Regulations and Guidelines for AI", "V8toOT2qCjE", "https://docs.google.com/presentation/d/1bQ0bwffG03BsJR2ARnojUb7JXl23x03-/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
    ]),
    ("Generative AI & Advanced Topics", [
        ("Generative AI: GANs & VAEs", "PLvXbxbjhCY", "https://docs.google.com/presentation/d/1QQ7A_Y1FISjM1UoUg0J5zAjopKZFYB79/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("AI in Edge Computing", "jxRTmyo_BHI", "https://docs.google.com/presentation/d/1gt2YG7Ve0jyC5q2nvHsKX12V-fOXomL8/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
        ("AI in Real-Time Systems", "tp2y1Lbm7_8", "https://docs.google.com/presentation/d/19EX4M_PG5LNhyzL5RkTZVhxKAykeArb-/edit?usp=drive_link&ouid=115205148767082075498&rtpof=true&sd=true", ""),
    ]),
    ("Capstone Project: Tweets Sentiment Analysis", [
        ("Capstone Project: Tweets Sentiment Analysis – Introduction & Dataset Loading", "YAlOE4UMcqA", "", "https://colab.research.google.com/drive/18g7Sh_GCktR0jnAhvwMYIa0EivUFjY72?usp=drive_link"),
        ("Capstone Project: Tweets Sentiment Analysis – Data Preprocessing", "uwYSWYs0jVY", "", "https://colab.research.google.com/drive/18g7Sh_GCktR0jnAhvwMYIa0EivUFjY72?usp=drive_link"),
        ("Capstone Project: Tweets Sentiment Analysis – Model Selection & Training", "NOS0AYuEMic", "", "https://colab.research.google.com/drive/18g7Sh_GCktR0jnAhvwMYIa0EivUFjY72?usp=drive_link"),
        ("Capstone Project: Tweets Sentiment Analysis – Streamlit Web App", "ww5ME10BKRk", "", "https://drive.google.com/file/d/1vRnuagQ7n_wj7CL9b4AlwsMtkDYKbxHY/view?usp=drive_link"),
    ]),
]

CAPSTONE_ASSIGNMENT_TITLE = "Capstone Project Assignment"
CAPSTONE_ASSIGNMENT_DESC = (
    "Build and deploy your own Tweets Sentiment Analysis project following "
    "the capstone module: load a dataset, preprocess the text, train and "
    "evaluate a model, then wrap it in a Streamlit app. Submit a link to "
    "your GitHub repo or deployed app."
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
