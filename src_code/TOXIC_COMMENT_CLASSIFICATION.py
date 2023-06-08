{
  "cells": [
    {
      "cell_type": "code",
      "execution_count": 4,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 178
        },
        "colab_type": "code",
        "id": "UDAYt1p5nFBB",
        "outputId": "f850cc9c-71cb-4ae9-ad6a-22ffc15fc4ac"
      },
      "outputs": [
        {
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'sklearn'",
          "output_type": "error",
          "traceback": [
            "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[1;32m<ipython-input-4-1aeeb3c25cb9>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m      7\u001b[0m \u001b[1;31m# !pip3 install bert-tensorflow\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      8\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m----> 9\u001b[1;33m \u001b[1;32mfrom\u001b[0m \u001b[0msklearn\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mmodel_selection\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mtrain_test_split\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     10\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mpandas\u001b[0m \u001b[1;32mas\u001b[0m \u001b[0mpd\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     11\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mtensorflow\u001b[0m \u001b[1;32mas\u001b[0m \u001b[0mtf\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
            "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'sklearn'"
          ]
        }
      ],
      "source": [
        "# %tensorflow_version 1.x\n",
        "import numpy as np \n",
        "import pandas as pd\n",
        "import os\n",
        "import collections\n",
        "\n",
        "# !pip3 install bert-tensorflow\n",
        "\n",
        "from sklearn.model_selection import train_test_split\n",
        "import pandas as pd\n",
        "import tensorflow as tf\n",
        "from tensorflow.contrib import rnn\n",
        "import tensorflow_hub as hub\n",
        "from datetime import datetime\n",
        "\n",
        "import bert\n",
        "from bert import run_classifier\n",
        "from bert import optimization\n",
        "from bert import tokenization\n",
        "from bert import modeling"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 5,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 336
        },
        "colab_type": "code",
        "id": "9hA2g4afp8o-",
        "outputId": "e8328547-39bd-479c-9b0a-541b3c10a132"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "--2020-05-29 08:49:17--  https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip\n",
            "Resolving storage.googleapis.com (storage.googleapis.com)... 173.194.216.128, 2607:f8b0:400c:c06::80\n",
            "Connecting to storage.googleapis.com (storage.googleapis.com)|173.194.216.128|:443... connected.\n",
            "HTTP request sent, awaiting response... 200 OK\n",
            "Length: 407727028 (389M) [application/zip]\n",
            "Saving to: ‘uncased_L-12_H-768_A-12.zip’\n",
            "\n",
            "uncased_L-12_H-768_ 100%[===================>] 388.84M   198MB/s    in 2.0s    \n",
            "\n",
            "2020-05-29 08:49:20 (198 MB/s) - ‘uncased_L-12_H-768_A-12.zip’ saved [407727028/407727028]\n",
            "\n",
            "Archive:  uncased_L-12_H-768_A-12.zip\n",
            "   creating: uncased_L-12_H-768_A-12/\n",
            "  inflating: uncased_L-12_H-768_A-12/bert_model.ckpt.meta  \n",
            "  inflating: uncased_L-12_H-768_A-12/bert_model.ckpt.data-00000-of-00001  \n",
            "  inflating: uncased_L-12_H-768_A-12/vocab.txt  \n",
            "  inflating: uncased_L-12_H-768_A-12/bert_model.ckpt.index  \n",
            "  inflating: uncased_L-12_H-768_A-12/bert_config.json  \n"
          ]
        }
      ],
      "source": [
        "!wget https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip\n",
        "!unzip uncased_L-12_H-768_A-12.zip"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "6pUPtiKSnFBG"
      },
      "outputs": [],
      "source": [
        "BERT_VOCAB= 'uncased_L-12_H-768_A-12/vocab.txt'\n",
        "BERT_INIT_CHKPNT = 'uncased_L-12_H-768_A-12/bert_model.ckpt'\n",
        "BERT_CONFIG = 'uncased_L-12_H-768_A-12/bert_config.json'"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "t8dleZlUnFBJ"
      },
      "outputs": [],
      "source": [
        "#tokenizer\n",
        "tokenization.validate_case_matches_checkpoint(True,BERT_INIT_CHKPNT)\n",
        "tokenizer = tokenization.FullTokenizer(vocab_file=BERT_VOCAB, do_lower_case=True)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "BGTiA1WmqgQo"
      },
      "outputs": [],
      "source": [
        "from google.colab import auth\n",
        "auth.authenticate_user()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 11,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 123
        },
        "colab_type": "code",
        "id": "MewPBEJmnFBM",
        "outputId": "acba3959-c7c2-4cec-c747-cc297c569ad0"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Copying gs://toxiccommentclassification/train.csv...\n",
            "- [1 files][ 65.6 MiB/ 65.6 MiB]                                                \n",
            "Operation completed over 1 objects/65.6 MiB.                                     \n",
            "Copying gs://toxiccommentclassification/test.csv...\n",
            "- [1 files][ 57.6 MiB/ 57.6 MiB]                                                \n",
            "Operation completed over 1 objects/57.6 MiB.                                     \n"
          ]
        }
      ],
      "source": [
        "!gsutil cp gs://toxiccommentclassification/train.csv train.csv\n",
        "!gsutil cp gs://toxiccommentclassification/test.csv test.csv\n",
        "train = pd.read_csv(\"train.csv\")\n",
        "test = pd.read_csv('test.csv')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 15,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 197
        },
        "colab_type": "code",
        "id": "Mt9d2y7AnFBP",
        "outputId": "970bc060-85ed-4b8c-a981-48e1845a4cc0"
      },
      "outputs": [
        {
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>id</th>\n",
              "      <th>comment_text</th>\n",
              "      <th>toxic</th>\n",
              "      <th>severe_toxic</th>\n",
              "      <th>obscene</th>\n",
              "      <th>threat</th>\n",
              "      <th>insult</th>\n",
              "      <th>identity_hate</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>55443</th>\n",
              "      <td>942801ad8f1f5557</td>\n",
              "      <td>don't thumbnail it, insert it like this,\\n 199...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>79997</th>\n",
              "      <td>d612437220d5df26</td>\n",
              "      <td>Thank you for your apology. I accept it, such ...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>133850</th>\n",
              "      <td>cc1228368707e0ea</td>\n",
              "      <td>You have a point, though I really like the rai...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>136954</th>\n",
              "      <td>dcb8e6555259c994</td>\n",
              "      <td>! IT WAS MENTIONED IN THE MOVIE THAT SHE WAS H...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>16116</th>\n",
              "      <td>2a8a60ea9f8cb544</td>\n",
              "      <td>Alpa Discucssion expansion \\n\\nHi SimonP\\n\\nI'...</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "                      id  ... identity_hate\n",
              "55443   942801ad8f1f5557  ...             0\n",
              "79997   d612437220d5df26  ...             0\n",
              "133850  cc1228368707e0ea  ...             0\n",
              "136954  dcb8e6555259c994  ...             0\n",
              "16116   2a8a60ea9f8cb544  ...             0\n",
              "\n",
              "[5 rows x 8 columns]"
            ]
          },
          "execution_count": 15,
          "metadata": {
            "tags": []
          },
          "output_type": "execute_result"
        }
      ],
      "source": [
        "train.sample(5)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "7U8H2kGonFBS"
      },
      "outputs": [],
      "source": [
        "ID = 'id'\n",
        "DATA_COLUMN = 'comment_text'\n",
        "LABEL_COLUMNS = ['toxic','severe_toxic','obscene','threat','insult','identity_hate']"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "1Zfw4K6-nFBU"
      },
      "outputs": [],
      "source": [
        "class InputExample(object):\n",
        "    def __init__(self, guid, text_a, text_b=None, labels=None):\n",
        "        self.guid = guid\n",
        "        self.text_a = text_a\n",
        "        self.text_b = text_b\n",
        "        self.labels = labels\n",
        "\n",
        "\n",
        "class InputFeatures(object):\n",
        "    def __init__(self, input_ids, input_mask, segment_ids, label_ids, is_real_example=True):\n",
        "        self.input_ids = input_ids\n",
        "        self.input_mask = input_mask\n",
        "        self.segment_ids = segment_ids\n",
        "        self.label_ids = label_ids,\n",
        "        self.is_real_example=is_real_example"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "jBRYkf0enFBY"
      },
      "outputs": [],
      "source": [
        "def create_examples(df, labels_available=True):\n",
        "    examples=[]\n",
        "    for (i, row) in enumerate(df.values):\n",
        "        guid = row[0]\n",
        "        text_a = row[1]\n",
        "        if labels_available:\n",
        "            labels = row[2:]\n",
        "        else:\n",
        "            labels = [0,0,0,0,0,0]\n",
        "        examples.append( InputExample(guid=guid, text_a=text_a, labels=labels))\n",
        "    return examples"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "NvU-65C-nFBb"
      },
      "outputs": [],
      "source": [
        "TRAIN_VAL_RATIO = 0.9\n",
        "LEN = train.shape[0]\n",
        "SIZE_TRAIN = int(TRAIN_VAL_RATIO*LEN)\n",
        "x_train = train[:SIZE_TRAIN]\n",
        "x_val = train[SIZE_TRAIN:]\n",
        "train_examples = create_examples(x_train)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "BrHItCsynFBe",
        "outputId": "0fdcbc49-95ec-4949-8d4e-11e503480b62"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "((159571, 8), (143613, 8), (15958, 8))"
            ]
          },
          "execution_count": 10,
          "metadata": {
            "tags": []
          },
          "output_type": "execute_result"
        }
      ],
      "source": [
        "train.shape, x_train.shape, x_val.shape"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "jmkBA3mBnFBg"
      },
      "outputs": [],
      "source": [
        "import pandas\n",
        "\n",
        "def convert_examples_to_features(examples,  max_seq_length, tokenizer):\n",
        "    features = []\n",
        "    for (ex_index, example) in enumerate(examples):\n",
        "        tokens_a = tokenizer.tokenize(example.text_a)\n",
        "        tokens_b = None\n",
        "        \n",
        "        if len(tokens_a) > max_seq_length - 2:\n",
        "            tokens_a = tokens_a[:(max_seq_length - 2)]\n",
        "        \n",
        "        tokens = [\"[CLS]\"] + tokens_a + [\"[SEP]\"]\n",
        "        segment_ids = [0] * len(tokens)\n",
        "        input_ids = tokenizer.convert_tokens_to_ids(tokens)\n",
        "        input_mask = [1] * len(input_ids)\n",
        "\n",
        "        padding = [0] * (max_seq_length - len(input_ids))\n",
        "        input_ids += padding\n",
        "        input_mask += padding\n",
        "        segment_ids += padding\n",
        "        \n",
        "        labels_ids = []\n",
        "        for label in example.labels:\n",
        "            labels_ids.append(int(label))\n",
        "        \n",
        "        inp_feat = InputFeatures(input_ids=input_ids,input_mask=input_mask,\n",
        "                                 segment_ids=segment_ids,label_ids=labels_ids)\n",
        "\n",
        "        features.append(inp_feat)\n",
        "        \n",
        "    return features"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "JR90gDYOnFBj"
      },
      "outputs": [],
      "source": [
        "# NEEDED FOR BERT SEQUENCE OUTPUT WITH ATTENTION\n",
        "class Attention(tf.keras.Model):\n",
        "    def __init__(self, units):\n",
        "        super(Attention, self).__init__()#trainable weights \n",
        "        self.W1 = tf.keras.layers.Dense(units)\n",
        "        self.W2 = tf.keras.layers.Dense(units)\n",
        "        self.V = tf.keras.layers.Dense(1)\n",
        "\n",
        "    def call(self, features, hidden):\n",
        "        #hidden shape == (batch_size, hidden size)\n",
        "        hidden_with_time_axis = tf.expand_dims(hidden, 1) #(8,1,768)\n",
        "\n",
        "        #score shape == (batch_size, max_length, 1)\n",
        "        score = tf.nn.tanh(self.W1(features) + self.W2(hidden_with_time_axis)) #(8,20,1)\n",
        "\n",
        "        #attention_weights shape == (batch_size, max_length, 1)\n",
        "        attention_weights = tf.nn.softmax(self.V(score), axis=1)      #(8,20,1)\n",
        "\n",
        "        #context_vector shape after sum == (batch_size, hidden_size\n",
        "        context_vector = attention_weights * features                #(8,20,768)\n",
        "        context_vector = tf.reduce_sum(context_vector, axis=1)       #(8,768)\n",
        "        return context_vector, attention_weights"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "FtXSNfmbnFBq"
      },
      "outputs": [],
      "source": [
        "def create_attention_model(bert_config, is_training, input_ids, input_mask, segment_ids,labels, num_labels, use_one_hot_embeddings):\n",
        "    model = modeling.BertModel(\n",
        "        config=bert_config,\n",
        "        is_training=is_training,\n",
        "        input_ids=input_ids,\n",
        "        input_mask=input_mask,\n",
        "        token_type_ids=segment_ids,\n",
        "        use_one_hot_embeddings=use_one_hot_embeddings)\n",
        "\n",
        "    #get sequence output from BERT \n",
        "    output_layer = model.get_sequence_output()\n",
        "\n",
        "    print(output_layer.shape)\n",
        "    \n",
        "    output_weights = tf.get_variable(\n",
        "        \"output_weights\", [num_labels, 768],\n",
        "        initializer=tf.truncated_normal_initializer(stddev=0.02))\n",
        "\n",
        "    output_bias = tf.get_variable(\n",
        "        \"output_bias\", [num_labels], initializer=tf.zeros_initializer())\n",
        "\n",
        "    with tf.variable_scope(\"loss\"):\n",
        "        #token embeddings of first 20 tokens \n",
        "        t1=output_layer[:,1:126]\n",
        "        print(t1.shape)\n",
        "        #token embedding of [CLS] token\n",
        "        t2=output_layer[:,0]\n",
        "\n",
        "        #compute context vector\n",
        "        context_vector, attention_weights = Attention(5)(t1,t2)\n",
        "        \n",
        "        #set the last layer to context vector\n",
        "        output_layer=context_vector\n",
        "\n",
        "        if is_training:\n",
        "            # I.e., 0.1 dropout\n",
        "            output_layer = tf.nn.dropout(output_layer, keep_prob=0.9)\n",
        "\n",
        "        #compute logits W.X+b\n",
        "        logits = tf.matmul(output_layer, output_weights, transpose_b=True)\n",
        "        logits = tf.nn.bias_add(logits, output_bias)\n",
        "\n",
        "        #compute sigmoid probabilities \n",
        "        probabilities = tf.nn.sigmoid(logits)\n",
        "        \n",
        "        #convert to float32\n",
        "        labels = tf.cast(labels, tf.float32)\n",
        "\n",
        "        #compute the loss\n",
        "        per_example_loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=labels, logits=logits)\n",
        "\n",
        "        loss = tf.reduce_mean(per_example_loss)\n",
        "\n",
        "        return (loss, per_example_loss, logits, probabilities)\n",
        "\n",
        "\n",
        "def create_lstm_model(bert_config, is_training, input_ids, input_mask, segment_ids,labels, num_labels, use_one_hot_embeddings):\n",
        "    model = modeling.BertModel(\n",
        "        config=bert_config,\n",
        "        is_training=is_training,\n",
        "        input_ids=input_ids,\n",
        "        input_mask=input_mask,\n",
        "        token_type_ids=segment_ids,\n",
        "        use_one_hot_embeddings=use_one_hot_embeddings)\n",
        "\n",
        "    #get sequence output from BERT \n",
        "    output_layer = model.get_sequence_output()\n",
        "\n",
        "    print(output_layer.shape)\n",
        "    \n",
        "    output_weights = tf.get_variable(\n",
        "        \"output_weights\", [num_labels, 768],\n",
        "        initializer=tf.truncated_normal_initializer(stddev=0.02))\n",
        "\n",
        "    output_bias = tf.get_variable(\n",
        "        \"output_bias\", [num_labels], initializer=tf.zeros_initializer())\n",
        "\n",
        "    with tf.variable_scope(\"loss\"):\n",
        "        #token embeddings of first 20 tokens \n",
        "        t1=output_layer[:,1:126]\n",
        "        print(t1.shape)\n",
        "        #token embedding of [CLS] token\n",
        "        t2=output_layer[:,0]\n",
        "\n",
        "        #compute lstm cell state vector\n",
        "        lstmcell =  tf.nn.rnn_cell.LSTMCell(768, state_is_tuple=True)\n",
        "        outputs, states = tf.nn.dynamic_rnn(lstmcell,\n",
        "                                  t1,\n",
        "                                  sequence_length=[20]*t1.shape[0].value,\n",
        "                                  dtype=tf.float32)\n",
        "    \n",
        "        output_layer=tf.reduce_mean([t2,states.h],0)  \n",
        "\n",
        "        if is_training:\n",
        "            # I.e., 0.1 dropout\n",
        "            output_layer = tf.nn.dropout(output_layer, keep_prob=0.9)\n",
        "\n",
        "        #compute logits W.X+b\n",
        "        logits = tf.matmul(output_layer, output_weights, transpose_b=True)\n",
        "        logits = tf.nn.bias_add(logits, output_bias)\n",
        "\n",
        "        #compute sigmoid probabilities \n",
        "        probabilities = tf.nn.sigmoid(logits)\n",
        "        \n",
        "        #convert to float32\n",
        "        labels = tf.cast(labels, tf.float32)\n",
        "\n",
        "        #compute the loss\n",
        "        per_example_loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=labels, logits=logits)\n",
        "\n",
        "        loss = tf.reduce_mean(per_example_loss)\n",
        "\n",
        "        return (loss, per_example_loss, logits, probabilities)\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "def create_simple_model(bert_config, is_training, input_ids, input_mask, segment_ids,labels, num_labels, use_one_hot_embeddings):\n",
        "    model = modeling.BertModel(\n",
        "        config=bert_config,\n",
        "        is_training=is_training,\n",
        "        input_ids=input_ids,\n",
        "        input_mask=input_mask,\n",
        "        token_type_ids=segment_ids,\n",
        "        use_one_hot_embeddings=use_one_hot_embeddings)\n",
        "\n",
        "    #get sequence output from BERT \n",
        "    output_layer = model.get_pooled_output()\n",
        "\n",
        "    print(output_layer.shape)\n",
        "    \n",
        "    output_weights = tf.get_variable(\n",
        "        \"output_weights\", [num_labels, 768],\n",
        "        initializer=tf.truncated_normal_initializer(stddev=0.02))\n",
        "\n",
        "    output_bias = tf.get_variable(\n",
        "        \"output_bias\", [num_labels], initializer=tf.zeros_initializer())\n",
        "\n",
        "    with tf.variable_scope(\"loss\"):\n",
        "\n",
        "        if is_training:\n",
        "            # I.e., 0.1 dropout\n",
        "            output_layer = tf.nn.dropout(output_layer, keep_prob=0.9)\n",
        "\n",
        "        #compute logits W.X+b\n",
        "        logits = tf.matmul(output_layer, output_weights, transpose_b=True)\n",
        "        logits = tf.nn.bias_add(logits, output_bias)\n",
        "\n",
        "        #compute sigmoid probabilities \n",
        "        probabilities = tf.nn.sigmoid(logits)\n",
        "        \n",
        "        #convert to float32\n",
        "        labels = tf.cast(labels, tf.float32)\n",
        "\n",
        "        #compute the loss\n",
        "        per_example_loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=labels, logits=logits)\n",
        "\n",
        "        loss = tf.reduce_mean(per_example_loss)\n",
        "\n",
        "        return (loss, per_example_loss, logits, probabilities)\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "def model_fn_builder(bert_config, num_labels, init_checkpoint, learning_rate,num_train_steps, num_warmup_steps, use_tpu,use_one_hot_embeddings,model_type=\"\"):\n",
        "\n",
        "    def model_fn(features, labels, mode, params): \n",
        "        \n",
        "\n",
        "        # input ids which are obtained from bert tokenizer\n",
        "        input_ids = features[\"input_ids\"]\n",
        "\n",
        "        # input masks to represent the actual sentence (1's along length of sentence , 0's for padding) and padding sequence\n",
        "        input_mask = features[\"input_mask\"]\n",
        "        \n",
        "        # segment ids to distinguish in case of two sentence tasks (not needed for this task)\n",
        "        segment_ids = features[\"segment_ids\"]\n",
        "\n",
        "        # label for sentence \n",
        "        label_ids = features[\"label_ids\"]\n",
        "\n",
        "        is_training = (mode == tf.estimator.ModeKeys.TRAIN)\n",
        "\n",
        "\n",
        "        if model_type==\"attention\":\n",
        "            (total_loss, per_example_loss, logits, probabilities) = create_attention_model(\n",
        "                          bert_config, is_training, input_ids, input_mask, segment_ids, label_ids,\n",
        "                          num_labels, use_one_hot_embeddings)\n",
        "        elif model_type==\"lstm\":\n",
        "            (total_loss, per_example_loss, logits, probabilities) = create_lstm_model(\n",
        "                          bert_config, is_training, input_ids, input_mask, segment_ids, label_ids,\n",
        "                          num_labels, use_one_hot_embeddings)\n",
        "        else:\n",
        "            (total_loss, per_example_loss, logits, probabilities) = create_simple_model(\n",
        "                          bert_config, is_training, input_ids, input_mask, segment_ids, label_ids,\n",
        "                          num_labels, use_one_hot_embeddings)\n",
        "\n",
        "        tvars = tf.trainable_variables()\n",
        "        initialized_variable_names = {}\n",
        "\n",
        "        if init_checkpoint:\n",
        "            (assignment_map, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars, init_checkpoint)\n",
        "            tf.train.init_from_checkpoint(init_checkpoint, assignment_map)\n",
        "\n",
        "        for var in tvars:\n",
        "            init_string = \"\"\n",
        "            if var.name in initialized_variable_names:\n",
        "                init_string = \", *INIT_FROM_CKPT*\"\n",
        "\n",
        "        output_spec = None\n",
        "\n",
        "        if mode == tf.estimator.ModeKeys.TRAIN:\n",
        "\n",
        "            train_op = optimization.create_optimizer(\n",
        "                total_loss, learning_rate, num_train_steps, num_warmup_steps, use_tpu)\n",
        "\n",
        "            output_spec = tf.estimator.EstimatorSpec(mode=mode,\n",
        "                                            loss=total_loss,\n",
        "                                            train_op=train_op,\n",
        "                                            scaffold=None)\n",
        "          \n",
        "        else:\n",
        "            output_spec = tf.estimator.EstimatorSpec(\n",
        "                mode=mode,\n",
        "                predictions={\"probabilities\": probabilities},\n",
        "                scaffold=None)\n",
        "        return output_spec\n",
        "\n",
        "    return model_fn"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "znqiDBnYnFBt"
      },
      "outputs": [],
      "source": [
        "BATCH_SIZE = 8\n",
        "LEARNING_RATE = 2e-5\n",
        "NUM_TRAIN_EPOCHS = 1.0\n",
        "WARMUP_PROPORTION = 0.1\n",
        "SAVE_CHECKPOINTS_STEPS = 1000\n",
        "SAVE_SUMMARY_STEPS = 500"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "cQEsPt4LnFBv"
      },
      "outputs": [],
      "source": [
        "OUTPUT_DIR = \"/content/output/output\"\n",
        "run_config = tf.estimator.RunConfig(\n",
        "    model_dir=OUTPUT_DIR,\n",
        "    save_summary_steps=SAVE_SUMMARY_STEPS,\n",
        "    keep_checkpoint_max=1,\n",
        "    save_checkpoints_steps=SAVE_CHECKPOINTS_STEPS)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "j4QVFJUDnFBy"
      },
      "outputs": [],
      "source": [
        "def input_fn_builder(features, seq_length, is_training, drop_remainder):\n",
        "\n",
        "    all_input_ids = []\n",
        "    all_input_mask = []\n",
        "    all_segment_ids = []\n",
        "    all_label_ids = []\n",
        "\n",
        "    for feature in features:\n",
        "        all_input_ids.append(feature.input_ids)\n",
        "        all_input_mask.append(feature.input_mask)\n",
        "        all_segment_ids.append(feature.segment_ids)\n",
        "        all_label_ids.append(feature.label_ids)\n",
        "\n",
        "    def input_fn(params):\n",
        "\n",
        "        batch_size = params[\"batch_size\"]\n",
        "\n",
        "        num_examples = len(features)\n",
        "\n",
        "        d = tf.data.Dataset.from_tensor_slices({\n",
        "            \"input_ids\":\n",
        "                tf.constant(\n",
        "                    all_input_ids, shape=[num_examples, seq_length],\n",
        "                    dtype=tf.int32),\n",
        "\n",
        "            \"input_mask\":\n",
        "                tf.constant(\n",
        "                    all_input_mask,\n",
        "                    shape=[num_examples, seq_length],\n",
        "                    dtype=tf.int32),\n",
        "\n",
        "            \"segment_ids\":\n",
        "                tf.constant(\n",
        "                    all_segment_ids,\n",
        "                    shape=[num_examples, seq_length],\n",
        "                    dtype=tf.int32),\n",
        "\n",
        "            \"label_ids\":\n",
        "                tf.constant(all_label_ids, shape=[num_examples, len(LABEL_COLUMNS)], dtype=tf.int32),\n",
        "        })\n",
        "\n",
        "        if is_training:\n",
        "            d = d.repeat()\n",
        "            d = d.shuffle(buffer_size=100)\n",
        "\n",
        "        d = d.batch(batch_size=batch_size, drop_remainder=drop_remainder)\n",
        "        return d\n",
        "\n",
        "    return input_fn"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "mJVjfLmVnFB0"
      },
      "outputs": [],
      "source": [
        "def convert_single_example(ex_index, example, max_seq_length,\n",
        "                           tokenizer):\n",
        "    \"\"\"Converts a single `InputExample` into a single `InputFeatures`.\"\"\"\n",
        "\n",
        "    if isinstance(example, DummyInputExample):\n",
        "        return InputFeatures(\n",
        "            input_ids=[0] * max_seq_length,\n",
        "            input_mask=[0] * max_seq_length,\n",
        "            segment_ids=[0] * max_seq_length,\n",
        "            label_ids=0,\n",
        "            is_real_example=False)\n",
        "\n",
        "    tokens_a = tokenizer.tokenize(example.text_a)\n",
        "    tokens_b = None\n",
        "    if example.text_b:\n",
        "        tokens_b = tokenizer.tokenize(example.text_b)\n",
        "    if len(tokens_a) > max_seq_length - 2:\n",
        "        tokens_a = tokens_a[0:(max_seq_length - 2)]\n",
        "\n",
        "    tokens = []\n",
        "    segment_ids = []\n",
        "    tokens.append(\"[CLS]\")\n",
        "    segment_ids.append(0)\n",
        "    for token in tokens_a:\n",
        "        tokens.append(token)\n",
        "        segment_ids.append(0)\n",
        "    tokens.append(\"[SEP]\")\n",
        "    segment_ids.append(0)\n",
        "\n",
        "    if tokens_b:\n",
        "        for token in tokens_b:\n",
        "            tokens.append(token)\n",
        "            segment_ids.append(1)\n",
        "        tokens.append(\"[SEP]\")\n",
        "        segment_ids.append(1)\n",
        "\n",
        "    input_ids = tokenizer.convert_tokens_to_ids(tokens)\n",
        "    input_mask = [1] * len(input_ids)\n",
        "\n",
        "    \n",
        "    while len(input_ids) < max_seq_length:\n",
        "        input_ids.append(0)\n",
        "        input_mask.append(0)\n",
        "        segment_ids.append(0)\n",
        "\n",
        "    labels_ids = []\n",
        "    for label in example.labels:\n",
        "        labels_ids.append(int(label))\n",
        "\n",
        "\n",
        "    feature = InputFeatures(\n",
        "        input_ids=input_ids,\n",
        "        input_mask=input_mask,\n",
        "        segment_ids=segment_ids,\n",
        "        label_ids=labels_ids,\n",
        "        is_real_example=True)\n",
        "    return feature\n",
        "\n",
        "\n",
        "def file_based_convert_examples_to_features(\n",
        "        examples, max_seq_length, tokenizer, output_file):\n",
        "    writer = tf.python_io.TFRecordWriter(output_file)\n",
        "\n",
        "    for (ex_index, example) in enumerate(examples):\n",
        "        feature = convert_single_example(ex_index, example,\n",
        "                                         max_seq_length, tokenizer)\n",
        "\n",
        "        def create_int_feature(values):\n",
        "            f = tf.train.Feature(int64_list=tf.train.Int64List(value=list(values)))\n",
        "            return f\n",
        "\n",
        "        features = collections.OrderedDict()\n",
        "        features[\"input_ids\"] = create_int_feature(feature.input_ids)\n",
        "        features[\"input_mask\"] = create_int_feature(feature.input_mask)\n",
        "        features[\"segment_ids\"] = create_int_feature(feature.segment_ids)\n",
        "        features[\"is_real_example\"] = create_int_feature(\n",
        "            [int(feature.is_real_example)])\n",
        "        if isinstance(feature.label_ids, list):\n",
        "            label_ids = feature.label_ids\n",
        "        else:\n",
        "            label_ids = feature.label_ids[0]\n",
        "        features[\"label_ids\"] = create_int_feature(label_ids)\n",
        "\n",
        "        tf_example = tf.train.Example(features=tf.train.Features(feature=features))\n",
        "        writer.write(tf_example.SerializeToString())\n",
        "    writer.close()\n",
        "\n",
        "\n",
        "def file_based_input_fn_builder(input_file, seq_length, is_training,\n",
        "                                drop_remainder):\n",
        "    \"\"\"Creates an `input_fn` closure to be passed to TPUEstimator.\"\"\"\n",
        "\n",
        "    name_to_features = {\n",
        "        \"input_ids\": tf.FixedLenFeature([seq_length], tf.int64),\n",
        "        \"input_mask\": tf.FixedLenFeature([seq_length], tf.int64),\n",
        "        \"segment_ids\": tf.FixedLenFeature([seq_length], tf.int64),\n",
        "        \"label_ids\": tf.FixedLenFeature([6], tf.int64),\n",
        "        \"is_real_example\": tf.FixedLenFeature([], tf.int64),\n",
        "    }\n",
        "\n",
        "    def _decode_record(record, name_to_features):\n",
        "        \"\"\"Decodes a record to a TensorFlow example.\"\"\"\n",
        "        example = tf.parse_single_example(record, name_to_features)\n",
        "\n",
        "        # tf.Example only supports tf.int64, but the TPU only supports tf.int32.\n",
        "        # So cast all int64 to int32.\n",
        "        for name in list(example.keys()):\n",
        "            t = example[name]\n",
        "            if t.dtype == tf.int64:\n",
        "                t = tf.to_int32(t)\n",
        "            example[name] = t\n",
        "\n",
        "        return example\n",
        "\n",
        "    def input_fn(params):\n",
        "        \"\"\"The actual input function.\"\"\"\n",
        "        batch_size = params[\"batch_size\"]\n",
        "\n",
        "        # For training, we want a lot of parallel reading and shuffling.\n",
        "        # For eval, we want no shuffling and parallel reading doesn't matter.\n",
        "        d = tf.data.TFRecordDataset(input_file)\n",
        "        if is_training:\n",
        "            d = d.repeat()\n",
        "            d = d.shuffle(buffer_size=100)\n",
        "\n",
        "        d = d.apply(\n",
        "            tf.contrib.data.map_and_batch(\n",
        "                lambda record: _decode_record(record, name_to_features),\n",
        "                batch_size=batch_size,\n",
        "                drop_remainder=drop_remainder))\n",
        "\n",
        "        return d\n",
        "\n",
        "    return input_fn\n",
        "\n",
        "\n",
        "def _truncate_seq_pair(tokens_a, tokens_b, max_length):\n",
        "\n",
        "    while True:\n",
        "        total_length = len(tokens_a) + len(tokens_b)\n",
        "        if total_length <= max_length:\n",
        "            break\n",
        "        if len(tokens_a) > len(tokens_b):\n",
        "            tokens_a.pop()\n",
        "        else:\n",
        "            tokens_b.pop()\n",
        "            \n",
        "class DummyInputExample(object):\n",
        "    pass"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 27,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        },
        "colab_type": "code",
        "id": "OA96fxdknFB3",
        "outputId": "3583479a-30bb-4ffa-a7df-c2a7128f8723"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "'train.tf_record'"
            ]
          },
          "execution_count": 27,
          "metadata": {
            "tags": []
          },
          "output_type": "execute_result"
        }
      ],
      "source": [
        "#from pathlib import Path\n",
        "train_file = os.path.join(\"train.tf_record\")\n",
        "#filename = Path(train_file)\n",
        "if not os.path.exists(train_file):\n",
        "    open(train_file, 'w').close()\n",
        "train_file"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 28,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        },
        "colab_type": "code",
        "id": "7bjj5K0bnFB6",
        "outputId": "e7ac1180-e9a9-4f32-d085-d39ed5910300"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "17951"
            ]
          },
          "execution_count": 28,
          "metadata": {
            "tags": []
          },
          "output_type": "execute_result"
        }
      ],
      "source": [
        "num_train_steps = int(len(train_examples) / BATCH_SIZE * NUM_TRAIN_EPOCHS)\n",
        "num_warmup_steps = int(num_train_steps * WARMUP_PROPORTION)\n",
        "num_train_steps"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 34,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 283
        },
        "colab_type": "code",
        "id": "0AxFgSiCsBYT",
        "outputId": "3034ab1f-331a-4a4a-9c47-d332ac80a68c"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Copying gs://toxiccommentclassification/output/checkpoint...\n",
            "Copying gs://toxiccommentclassification/output/events.out.tfevents.1590732301.toxic...\n",
            "Copying gs://toxiccommentclassification/output/graph.pbtxt...\n",
            "Copying gs://toxiccommentclassification/output/model.ckpt-17951.data-00000-of-00001...\n",
            "/ [4 files][  1.2 GiB/  1.2 GiB]   75.0 MiB/s                                   \n",
            "==> NOTE: You are performing a sequence of gsutil operations that may\n",
            "run significantly faster if you instead use gsutil -m cp ... Please\n",
            "see the -m section under \"gsutil help options\" for further information\n",
            "about when gsutil -m can be advantageous.\n",
            "\n",
            "Copying gs://toxiccommentclassification/output/model.ckpt-17951.index...\n",
            "Copying gs://toxiccommentclassification/output/model.ckpt-17951.meta...\n",
            "Copying gs://toxiccommentclassification/output/train.tf_record...\n",
            "\\ [7 files][  1.3 GiB/  1.3 GiB]   69.2 MiB/s                                   \n",
            "Operation completed over 7 objects/1.3 GiB.                                      \n"
          ]
        }
      ],
      "source": [
        "!gsutil cp -r gs://toxiccommentclassification/output/ output"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "fopEqq1jnFB8"
      },
      "outputs": [],
      "source": [
        "MAX_SEQ_LENGTH=128\n",
        "file_based_convert_examples_to_features(train_examples, MAX_SEQ_LENGTH, tokenizer, train_file)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "pXE92DkxnFB-"
      },
      "outputs": [],
      "source": [
        "MAX_SEQ_LENGTH=128\n",
        "train_input_fn = file_based_input_fn_builder(\n",
        "                input_file=train_file,\n",
        "                seq_length=MAX_SEQ_LENGTH,\n",
        "                is_training=True,\n",
        "                drop_remainder=True)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 41,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 161
        },
        "colab_type": "code",
        "id": "HR0ng_uenFCA",
        "outputId": "c9f1798b-3713-4674-90b9-27db1bc27428"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "INFO:tensorflow:Using config: {'_model_dir': '/content/output/output', '_tf_random_seed': None, '_save_summary_steps': 500, '_save_checkpoints_steps': 1000, '_save_checkpoints_secs': None, '_session_config': allow_soft_placement: true\n",
            "graph_options {\n",
            "  rewrite_options {\n",
            "    meta_optimizer_iterations: ONE\n",
            "  }\n",
            "}\n",
            ", '_keep_checkpoint_max': 1, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_service': None, '_cluster_spec': <tensorflow.python.training.server_lib.ClusterSpec object at 0x7fc9a4ba4630>, '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}\n"
          ]
        }
      ],
      "source": [
        "bert_config = modeling.BertConfig.from_json_file(BERT_CONFIG)\n",
        "model_fn = model_fn_builder(\n",
        "  bert_config=bert_config,\n",
        "  num_labels= len(LABEL_COLUMNS),\n",
        "  init_checkpoint=BERT_INIT_CHKPNT,\n",
        "  learning_rate=LEARNING_RATE,\n",
        "  num_train_steps=num_train_steps,\n",
        "  num_warmup_steps=num_warmup_steps,\n",
        "  use_tpu=False,\n",
        "  use_one_hot_embeddings=False,\n",
        "  model_type=\"attention\")\n",
        "\n",
        "estimator = tf.estimator.Estimator(\n",
        "  model_fn=model_fn,\n",
        "  config=run_config,\n",
        "  params={\"batch_size\":BATCH_SIZE})"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 42,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 52
        },
        "colab_type": "code",
        "id": "OkzQGl4snFCC",
        "outputId": "cffff1cc-9a7f-466d-d7d0-39c2e467b65c"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "INFO:tensorflow:Skipping training since max_steps has already saved.\n"
          ]
        },
        {
          "data": {
            "text/plain": [
              "<tensorflow_estimator.python.estimator.estimator.Estimator at 0x7fc9a4ba44e0>"
            ]
          },
          "execution_count": 42,
          "metadata": {
            "tags": []
          },
          "output_type": "execute_result"
        }
      ],
      "source": [
        "estimator.train(input_fn=train_input_fn, max_steps=num_train_steps)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 108,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 267
        },
        "colab_type": "code",
        "id": "8GD0H1aKnFCE",
        "outputId": "09201249-cd24-41f9-d9b1-2b5b704495fe"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "enter text:Pakistan terrorists are planning to kill Indians \n",
            "WARNING:tensorflow:Entity <function file_based_input_fn_builder.<locals>.input_fn.<locals>.<lambda> at 0x7fc9b27f0730> could not be transformed and will be executed as-is. Please report this to the AutoGraph team. When filing the bug, set the verbosity to 10 (on Linux, `export AUTOGRAPH_VERBOSITY=10`) and attach the full output. Cause: module 'gast' has no attribute 'Str'\n",
            "WARNING: Entity <function file_based_input_fn_builder.<locals>.input_fn.<locals>.<lambda> at 0x7fc9b27f0730> could not be transformed and will be executed as-is. Please report this to the AutoGraph team. When filing the bug, set the verbosity to 10 (on Linux, `export AUTOGRAPH_VERBOSITY=10`) and attach the full output. Cause: module 'gast' has no attribute 'Str'\n",
            "INFO:tensorflow:Calling model_fn.\n",
            "(?, 128, 768)\n",
            "(?, 125, 768)\n",
            "WARNING:tensorflow:Entity <bound method Attention.call of <__main__.Attention object at 0x7fc9b1730a20>> could not be transformed and will be executed as-is. Please report this to the AutoGraph team. When filing the bug, set the verbosity to 10 (on Linux, `export AUTOGRAPH_VERBOSITY=10`) and attach the full output. Cause: Bad argument number for Name: 3, expecting 4\n",
            "WARNING: Entity <bound method Attention.call of <__main__.Attention object at 0x7fc9b1730a20>> could not be transformed and will be executed as-is. Please report this to the AutoGraph team. When filing the bug, set the verbosity to 10 (on Linux, `export AUTOGRAPH_VERBOSITY=10`) and attach the full output. Cause: Bad argument number for Name: 3, expecting 4\n",
            "INFO:tensorflow:Done calling model_fn.\n",
            "INFO:tensorflow:Graph was finalized.\n",
            "INFO:tensorflow:Restoring parameters from /content/output/output/model.ckpt-17951\n",
            "INFO:tensorflow:Running local_init_op.\n",
            "INFO:tensorflow:Done running local_init_op.\n"
          ]
        }
      ],
      "source": [
        "inp=input(\"enter text:\")\n",
        "data=[[\"100aaa\",inp]]\n",
        "test=pd.DataFrame(data=data,columns=[\"id\",\"comment_text\"])\n",
        "test_examples = create_examples(test,False)\n",
        "test_file=\"test.tf_record\"\n",
        "file_based_convert_examples_to_features(test_examples, MAX_SEQ_LENGTH, tokenizer, test_file)\n",
        "predict_input_fn = file_based_input_fn_builder(\n",
        "    input_file=test_file,\n",
        "    seq_length=MAX_SEQ_LENGTH,\n",
        "    is_training=False,\n",
        "    drop_remainder=False)\n",
        "predictions = estimator.predict(predict_input_fn)\n",
        "probabilities=None\n",
        "for it in predictions:\n",
        "  probabilities=it[\"probabilities\"]"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 109,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 570
        },
        "colab_type": "code",
        "id": "8HnyNbw5uOCk",
        "outputId": "d5542b6b-5c3d-4699-c4eb-7d9d831287c5"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "CATEGORY::::PROBABILITY\n",
            "toxic::::0.89419854\n",
            "severe_toxic::::0.045063224\n",
            "obscene::::0.14746724\n",
            "threat::::0.09462587\n",
            "insult::::0.20482463\n",
            "identity_hate::::0.69885457\n"
          ]
        },
        {
          "data": {
            "text/plain": [
              "<BarContainer object of 6 artists>"
            ]
          },
          "execution_count": 109,
          "metadata": {
            "tags": []
          },
          "output_type": "execute_result"
        },
        {
          "data": {
            "image/png": "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",
            "text/plain": [
              "<Figure size 504x504 with 1 Axes>"
            ]
          },
          "metadata": {
            "needs_background": "light",
            "tags": []
          },
          "output_type": "display_data"
        }
      ],
      "source": [
        "print(\"CATEGORY::::PROBABILITY\")\n",
        "for k,v in zip(LABEL_COLUMNS,probabilities):\n",
        "  print(k,v,sep=\"::::\")\n",
        "import matplotlib.pyplot as plt\n",
        "import numpy as np\n",
        "plt.figure(figsize=(7,7))\n",
        "plt.xticks(np.arange(0,1,0.2))\n",
        "plt.barh(LABEL_COLUMNS,probabilities)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "87no31cDuXNu"
      },
      "outputs": [],
      "source": []
    }
  ],
  "metadata": {
    "colab": {
      "name": "BERT_TOXIC_COMMENT_CLASSIFICATION.ipynb",
      "provenance": []
    },
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.8.5"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}
