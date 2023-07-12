# ExamOn

## Prequisites

* Python 3.9.15 or later
* Pip

## Quick Start

```shell
pip install examon
examon repo add pcap1
examon repo add_active pcap1
examon repo install
examon quiz 
```

### Customising Your Exam

#### Set the active repos

Examon will only use questions from repositories added which have been marked as active

```shell
examon repos list
examon repos add_active <repo name>
```
* Use the tag filter

## Active Exam Repositories

| Description | Pip Package |
|-------------|-------------|
| Beginners   ||
| PCEP 1      ||
| PCAP 1      ||
| PCAP 2      ||
| PCAP 3      ||
| PCAP 4      ||

## Creating your own Exam

### Install from Pypi

### Install from GitHub

## Roadmap

### V1.1

* Filter questions by multiple tags
* Filter questions by difficulty
* Filter questions by LOC
* Add time on question results