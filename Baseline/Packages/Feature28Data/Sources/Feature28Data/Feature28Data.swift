import Feature28Domain

public enum Feature28DataRepository {
    public static func load(_ id: Int) -> Feature28DomainModel {
        Feature28DomainModel(id: id, title: "Feature 28")
    }
}
