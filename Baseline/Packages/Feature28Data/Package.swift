// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature28Data",
    products: [.library(name: "Feature28Data", targets: ["Feature28Data"])],
    dependencies: [.package(path: "../Feature28Domain")],
    targets: [.target(name: "Feature28Data", dependencies: [.product(name: "Feature28Domain", package: "Feature28Domain")])]
)
