// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature01Presentation",
    products: [.library(name: "Feature01Presentation", targets: ["Feature01Presentation"])],
    dependencies: [.package(path: "../Feature01Domain"),
        .package(path: "../Feature01Data")],
    targets: [.target(name: "Feature01Presentation", dependencies: [.product(name: "Feature01Domain", package: "Feature01Domain"), .product(name: "Feature01Data", package: "Feature01Data")])]
)
